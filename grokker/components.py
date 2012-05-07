import venusian

SENTINEL = object()

class DirectiveValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg

def make_arguments(directives, ob):
    result = {}
    for directive in directives:
        value = directive.get(ob)
        if value is SENTINEL:
            continue
        result[directive.name] = value
    return result

class MetaGrokker(object):
    category = None
    
    def __call__(self, grokker):
        # get the directives this grokker wants
        directives = make_arguments([directive], grokker)['directive']
        def wrapped_grokker(wrapped):
            kw = make_arguments(directives, wrapped)
            def callback(scanner, name, ob):
                # XXX give better feedback identifying grokker in
                # case of a TypeError
                grokker(scanner, name, ob, **kw)
            venusian.attach(wrapped, callback, category=self.category)
            return wrapped
        return wrapped_grokker

grokker = MetaGrokker()

class BaseDirective(object):
    def __init__(self, name, module_name, converter=None, validator=None,
                 set_policy=setattr, get_policy=getattr,
                 default_policy=None):
        self.name = name
        self.module_name = module_name
        self.dotted_name = module_name + '.' + name
        self.converter = converter
        self.validator = validator
        self.set_policy = set_policy
        self.get_policy = get_policy
        self.default_policy = default_policy
        
    def get(self, ob):
        result = self.get_policy(ob, self.dotted_name, SENTINEL)
        if result is SENTINEL and self.default_policy is not None:
            result = self.default_policy()
        return result
    
class Directive(BaseDirective):
    
    def __call__(self, value):
        def wrapper(wrapped):
            if self.converter is not None:
                converted_value = self.converter(value)
            else:
                converted_value = value
            if self.validator is not None:
                self.validator(self.dotted_name, converted_value)
            self.set_policy(wrapped, self.dotted_name, converted_value)
            return wrapped
        return wrapper

class ArgsDirective(BaseDirective):
    
    def __call__(self, *args):
        def wrapper(wrapped):
            if self.converter is not None:
                converted_args = []
                for arg in args:
                    converted_args.append(self.converter(arg))
            else:
                converted_args = args
            if self.validator is not None:
                for arg in converted_args:
                    self.validator(self.dotted_name, converted_value)
            self.set_policy(wrapped, self.dotted_name, converted_args)
            return wrapped
        return wrapper

def list_set_policy(obj, name, value):
    l = obj.__dict__.get(name, None)
    if l is None:
        l = []
        setattr(obj, name, l)
    l.append(value)

def list_get_policy(obj, name, default):
    mro = getattr(obj, 'mro', None)
    if mro is None:
        return getattr(obj, name)
    result = []
    for base in obj.mro():
        l = base.__dict__.get(name, None)
        if l is not None and l not in result:
            result.append(l)
    result_flattened = []
    for entry in result:
        result_flattened.extend(entry)
    return result_flattened

directive = Directive('directive', __name__,
                      set_policy=list_set_policy,
                      get_policy=list_get_policy)

