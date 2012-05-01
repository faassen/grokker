import venusian

class DirectiveValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg

def make_arguments(directives, ob):
    result = {}
    for directive in directives:
        result[directive.name] = directive.get(ob)
    return result

class MetaGrokker(object):
    category = None
    
    def __call__(self, grokker):
        # get the directives this grokker wants
        directives = make_arguments([directive], grokker)['directive']
        def wrapped_grokker(wrapped):
            kw = make_arguments(directives, wrapped)
            def callback(scanner, name, ob):
                grokker(scanner, name, ob, **kw)
            venusian.attach(wrapped, callback, category=self.category)
            return wrapped
        return wrapped_grokker

grokker = MetaGrokker()

class Directive(object):
    def __init__(self, name, module_name, validator=None,
                 set_policy=setattr, get_policy=getattr):
        self.name = name
        self.module_name = module_name
        self.dotted_name = module_name + '.' + name
        self.validator = validator
        self.set_policy = set_policy
        self.get_policy = get_policy

    def get(self, ob):
        return self.get_policy(ob, self.dotted_name)
    
    def __call__(self, value):
        def wrapper(wrapped):
            if self.validator is not None:
                self.validator(self.dotted_name, value)
            self.set_policy(wrapped, self.dotted_name, value)
            return wrapped
        return wrapper

def list_set_policy(obj, name, value):
    l = obj.__dict__.get(name, None)
    if l is None:
        l = []
        setattr(obj, name, l)
    l.append(value)

def list_get_policy(obj, name):
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

