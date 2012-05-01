from grokker import Directive, directive, grokker

bar = Directive('bar', __name__)

@grokker
@directive(bar)
# no bar='default' keyword argument is supplied
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
# so cannot interpret this, as no explicit bar given
class SomeClass(object):
    pass
