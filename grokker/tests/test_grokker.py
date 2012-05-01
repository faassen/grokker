import venusian

def test_grokker_directive():
    from .fixtures import grokker_directive
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(grokker_directive)

    assert grokked == [
        ('SomeClass', grokker_directive.SomeClass, 'the bar value')]
    
