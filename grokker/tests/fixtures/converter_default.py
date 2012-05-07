from grokker import Directive, directive, grokker

def converter(value):
    if value is None:
        return "default"
    return value

bar = Directive('bar', __name__, converter=converter)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
class A(object):
    pass

@foo
@bar('not default')
class B(object):
    pass
