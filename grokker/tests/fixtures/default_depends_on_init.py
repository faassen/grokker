from grokker import Directive, directive, grokker, SENTINEL

initialized = False

def initialize():
    global initialized
    initialized = True

def converter(value):
    if initialized:
        return "initialized"
    else:
        return "not initialized"

bar = Directive('bar', __name__, converter=converter)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
class A(object):
    pass
