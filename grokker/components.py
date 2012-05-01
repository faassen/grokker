import venusian

def make_arguments(directives, ob):
    result = {}
    for directive in directives:
        result[directive.name] = directive.get(ob)
    return result

# class Grokker(object):
#     category = None

#     directives = []
    
#     def callback(self, scanner, name, ob):
#         kw = make_arguments(self.directives, ob)
#         self.grok(scanner.grokked, name, ob, **kw)
        
#     def grok(self, grokked, name, ob, **kw):
#         raise NotImplementedError
    
#     def __call__(self, wrapped):
#         venusian.attach(wrapped, self.callback, category=self.category)
#         return wrapped

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
    def __init__(self, name, storage_policy=setattr):
        self.name = name
        self.storage_policy = storage_policy
        
    def get(self, ob):
        return getattr(ob, self.name)
    
    def __call__(self, value):
        def wrapper(wrapped):
            self.storage_policy(wrapped, self.name, value)
            return wrapped
        return wrapper

def list_storage_policy(obj, name, value):
    l = getattr(obj, name, None)
    if l is None:
        l = []
        setattr(obj, name, l)
    l.append(value)

directive = Directive('directive', storage_policy=list_storage_policy)
    
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
