from grokker import (Directive, directive, grokker, list_set_policy,
                     list_get_policy)

bar = Directive('bar', set_policy=list_set_policy,
                get_policy=list_get_policy)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
@bar("first bar")
@bar("second bar")
class Alpha(object):
    pass

@foo
class Beta(Alpha):
    pass

@foo
@bar("third bar")
class Gamma(Alpha):
    pass

@foo
class Delta(object):
    pass
