import venusian

def test_grokker():
    from .fixtures import one
    
    grokked = []
    scanner = venusian.Scanner(grokked=grokked)
    scanner.scan(one)

    assert grokked == [('SomeClass', one.SomeClass, 'the bar value')]
    
