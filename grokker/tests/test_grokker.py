import venusian
from grokker import validator
import py.test

def test_grokker_directive():
    from .fixtures import grokker_directive as module
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    assert grokked == [
        ('SomeClass', module.SomeClass, 'the bar value')]

def test_mangled_name():
    from .fixtures import grokker_directive as module

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)
    
    assert (getattr(module.SomeClass,
                    'grokker.tests.fixtures.grokker_directive.bar') ==
            'the bar value')
    
def test_list_storage():
    from .fixtures import list_storage as module

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    assert grokked == [
        ('Alpha', module.Alpha, ['second bar', 'first bar']),
        ('Beta', module.Beta, ['second bar', 'first bar']),
        ('Delta', module.Delta, []),
        ('Gamma', module.Gamma, ['third bar', 'second bar', 'first bar']),
        ]

def test_directive_name_and_dotted_name():
    from .fixtures import grokker_directive as module

    assert module.bar.name == 'bar'
    assert (module.bar.dotted_name ==
            'grokker.tests.fixtures.grokker_directive.bar')
    
def test_validator():
    with py.test.raises(validator.GrokkerValidationError) as e:
        from .fixtures import str_validator
        str_validator # pyflakes
    assert str(e.value) == (
        "The 'grokker.tests.fixtures.str_validator.bar' "
        "directive can only be called with a unicode or str argument.")
    

def test_argsdirective():
    from .fixtures import argsdirective as module

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    assert grokked == [
        ('SomeClass', module.SomeClass, ('one', 'two')),
        ]

# XXX try argsdirective with converter and validator
    
def test_default():
    from .fixtures import default as module
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    assert grokked == [
        ('SomeClass', module.SomeClass, "default"),
        ]

def test_default_no_args_default():
    from .fixtures import no_args_default as module
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    with py.test.raises(TypeError):
        scanner.scan(module)

def test_directive_default():
    from .fixtures import directive_default as module

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    a, b = grokked

    name, obj, bar = a
    assert bar == 'default'
    name, obj, bar = b
    assert bar == 'not default'
    
def test_converter():
    from .fixtures import converter as module

    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(module)

    grokked = sorted(grokked)

    a, b = grokked

    name, obj, bar = a
    assert bar == 6
    name, obj, bar = b
    assert bar == 6

def test_conversion_before_validation():
    with py.test.raises(validator.GrokkerValidationError) as e:
        from .fixtures import convertthenvalidate as module
    
# converter for default depending on a global being initialized
# during configuration time, import order issue


# XXX need a test for default policy on grokker too
# and interactions with default arg versus default policy

