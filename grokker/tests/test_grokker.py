import venusian
from grokker import validator
import py.test

def test_grokker_directive():
    from .fixtures import grokker_directive
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(grokker_directive)

    assert grokked == [
        ('SomeClass', grokker_directive.SomeClass, 'the bar value')]

def test_mangled_name():
    from .fixtures import grokker_directive

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(grokker_directive)

    assert (getattr(grokker_directive.SomeClass,
                    'grokker.tests.fixtures.grokker_directive.bar') ==
            'the bar value')
    
def test_list_storage():
    from .fixtures import list_storage

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(list_storage)

    assert grokked == [
        ('Alpha', list_storage.Alpha, ['second bar', 'first bar']),
        ('Beta', list_storage.Beta, ['second bar', 'first bar']),
        ('Delta', list_storage.Delta, []),
        ('Gamma', list_storage.Gamma, ['third bar', 'second bar', 'first bar']),
        ]

def test_directive_name_and_dotted_name():
    from .fixtures import grokker_directive

    assert grokker_directive.bar.name == 'bar'
    assert (grokker_directive.bar.dotted_name ==
            'grokker.tests.fixtures.grokker_directive.bar')
    
def test_validator():
    with py.test.raises(validator.GrokkerValidationError) as e:
        from .fixtures import str_validator
    assert str(e.value) == (
        "The 'grokker.tests.fixtures.str_validator.bar' "
        "directive can only be called with a unicode or str argument.")
    

def test_argsdirective():
    from .fixtures import argsdirective

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(argsdirective)

    assert grokked == [
        ('SomeClass', argsdirective.SomeClass, ('one', 'two')),
        ]
        
