import pytest
from enhancement.ndict import ndict

@pytest.fixture
def empty_dict():
    """Create an empty ndict."""
    return ndict()

@pytest.fixture
def simple_dict():
    """Create a simple ndict with basic key-value pairs."""
    return ndict({'a': 1, 'b': 2})

@pytest.fixture
def nested_dict():
    """Create a nested ndict with multiple levels."""
    d = ndict()
    d['x']['y']['z'] = 3
    d['p']['q'] = 4
    return d

def test_auto_nesting():
    """Test automatic creation of nested dictionaries."""
    d = ndict()
    d['a']['b']['c'] = 1
    
    assert isinstance(d['a'], ndict)
    assert isinstance(d['a']['b'], ndict)
    assert d['a']['b']['c'] == 1
    
    # Test accessing non-existent keys
    assert isinstance(d['x']['y'], ndict)
    assert len(d['x']['y']) == 0

def test_extract():
    """Test the extract method for leaf values."""
    d = ndict()
    d['a'] = 1
    d['b']['c'] = 2
    d['b']['d']['e'] = 3
    
    # Test with new list
    result = d.extract()
    assert sorted(result) == [1, 2, 3]
    
    # Test with provided list
    existing = [0]
    result = d.extract(existing)
    assert sorted(result) == [0, 1, 2, 3]
    
    # Test with empty nested dictionary
    empty = ndict()
    empty['a']['b'] = ndict()
    assert empty.extract() == []

def test_extract_all():
    """Test the extract_all static method."""
    # Test with mixed dictionary types
    d = {
        'a': 1,
        'b': {'c': 2},
        'd': ndict({'e': {'f': 3}})
    }
    
    result = ndict.extract_all(d)
    assert sorted(result) == [1, 2, 3]
    
    # Test circular reference
    circular = {}
    circular['a'] = circular
    result = ndict.extract_all(circular)
    assert result == []

def test_flatten():
    """Test the flatten method."""
    d = ndict()
    d['a'] = 1
    d['b']['c'] = 2
    d['b']['d']['e'] = 3
    
    # Test basic flattening
    result = d.flatten()
    expected = {
        'a': 1,
        'b_c': 2,
        'b_d_e': 3
    }
    assert result == expected
    
    # Test with custom separator
    result = d.flatten(sep='.')
    expected = {
        'a': 1,
        'b.c': 2,
        'b.d.e': 3
    }
    assert result == expected
    
    # Test with existing dictionary
    existing = {'x': 0}
    result = d.flatten(flattened=existing)
    assert 'x' in result
    assert result['x'] == 0

def test_flatten_all():
    """Test the flatten_all static method."""
    # Test with mixed dictionary types
    d = {
        'a': 1,
        'b': {'c': 2},
        'd': ndict({'e': {'f': 3}})
    }
    
    result = ndict.flatten_all(d)
    expected = {
        'a': 1,
        'b_c': 2,
        'd_e_f': 3
    }
    assert result == expected
    
    # Test with custom separator
    result = ndict.flatten_all(d, sep='/')
    expected = {
        'a': 1,
        'b/c': 2,
        'd/e/f': 3
    }
    assert result == expected

def test_edge_cases():
    """Test edge cases and potential error conditions."""
    d = ndict()
    
    # Test with None values
    d['a'] = None
    assert d['a'] is None
    
    # Test with empty string keys
    d['']['b'] = 1
    assert d['']['b'] == 1
    
    # Test with integer keys
    d[1][2][3] = 'test'
    assert d[1][2][3] == 'test'
    
    # Test with tuple keys (should work as they're hashable)
    d[(1, 2)][(3, 4)] = 'tuple'
    assert d[(1, 2)][(3, 4)] == 'tuple'

def test_circular_references():
    """Test handling of circular references."""
    d = ndict()
    d['a'] = d
    
    # Test extract with circular reference
    result = d.extract()
    assert result == []
    
    # Test flatten with circular reference
    result = d.flatten()
    assert result == {} 