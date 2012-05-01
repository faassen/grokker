from grokker import ArgsDirective, directive, grokker

bar = ArgsDirective('bar', __name__)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
@bar("one", "two")
class SomeClass(object):
    pass

