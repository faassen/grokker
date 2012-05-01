from grokker import Directive, directive, grokker

bar = Directive('bar', __name__)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar='default'):
    scanner.grokked.append((name, ob, bar))
    
@foo
class SomeClass(object):
    pass
