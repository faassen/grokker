import venusian

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
    def __init__(self, name, set_policy=setattr, get_policy=getattr):
        self.name = name
        self.set_policy = set_policy
        self.get_policy = get_policy
        
    def get(self, ob):
        return self.get_policy(ob, self.name)
    
    def __call__(self, value):
        def wrapper(wrapped):
            self.set_policy(wrapped, self.name, value)
            return wrapped
        return wrapper

def list_set_policy(obj, name, value):
    l = getattr(obj, name, None)
    if l is None:
        l = []
        setattr(obj, name, l)
    l.append(value)

directive = Directive('directive', set_policy=list_set_policy)
    
# class Grokker(object):
#     category = None
    
#     def __init__(self):
#         pass
    
#     def grok(self, name, obj, **kw):
#         raise NotImplemented
    
#     def __call__(self, wrapped):
#         venusian.attach(wrapped, self.grok, category=self.category)
#         return wrapped
    
# class Directive(object):
#     pass

# class Storer(object):
#     pass
