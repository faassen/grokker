from grokker import (Directive, directive, grokker, validator,
                     GrokkerValidationError)

def validator(dottedname, value):
    assert isinstance(value, int)
    if not value > 6:
        raise GrokkerValidationError("%s: Value should be greater than 6" %
                                     dottedname)

def converter(value):
    return int(value)

bar = Directive('bar', __name__, converter=converter, validator=validator)

@grokker
@directive(bar)
def foo(scanner, name, ob, bar):
    scanner.grokked.append((name, ob, bar))
    
@foo
@bar('5')
class A(object):
    pass

