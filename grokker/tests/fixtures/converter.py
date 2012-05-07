from grokker import Directive, directive, grokker

def converter(value):
    return value + 1

bar = Directive('bar', __name__, converter=converter)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
@bar(5)
class A(object):
    pass

@foo
class B(A):
    pass

