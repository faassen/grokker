from grokker import Directive, directive, grokker

def default_policy():
    return 'default'

bar = Directive('bar', __name__,
                default_policy=default_policy)

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
