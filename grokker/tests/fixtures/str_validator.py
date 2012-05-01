from grokker import Directive, directive, grokker, validator

bar = Directive('bar', __name__, validator=validator.str_validator)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
@bar(5) # this will fail
class SomeClass(object):
    pass

