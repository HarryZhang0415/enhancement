import pytest
from enhancement.iterable import Iterable, IterableList

@pytest.fixture
def iterable():
    """Fixture that provides an Iterable instance."""
    return Iterable()

@pytest.fixture
def iterable_list():
    """Fixture that provides an IterableList instance."""
    return IterableList()

def test_iterable_init(iterable):
    """Test initialization of Iterable."""
    assert len(iterable) == 0

def test_iterable_setitem_getitem(iterable):
    """Test setting and getting items."""
    iterable['key'] = 'value'
    assert iterable['key'] == 'value'
    
    # Test nested access (should work due to ndict)
    iterable['a']['b']['c'] = 'nested'
    assert iterable['a']['b']['c'] == 'nested'
    
    # Test with different value types
    iterable['int'] = 42
    iterable['float'] = 3.14
    iterable['list'] = [1, 2, 3]
    iterable['dict'] = {'x': 1}
    
    assert iterable['int'] == 42
    assert iterable['float'] == 3.14
    assert iterable['list'] == [1, 2, 3]
    assert iterable['dict'] == {'x': 1}

def test_iterable_contains(iterable):
    """Test membership testing."""
    iterable['key'] = 'value'
    assert 'key' in iterable
    assert 'nonexistent' not in iterable

def test_iterable_len(iterable):
    """Test length calculation."""
    assert len(iterable) == 0
    iterable['key1'] = 'value1'
    iterable['key2'] = 'value2'
    assert len(iterable) == 2

def test_iterable_iter(iterable):
    """Test iteration."""
    test_data = {'key1': 'value1', 'key2': 'value2'}
    for k, v in test_data.items():
        iterable[k] = v
    
    # Test that we can iterate over keys
    iterated_keys = set(iterable)
    assert iterated_keys == set(test_data.keys())

def test_iterable_keys_items_values(iterable):
    """Test keys, items, and values methods."""
    test_data = {'key1': 'value1', 'key2': 'value2'}
    for k, v in test_data.items():
        iterable[k] = v
    
    assert set(iterable.keys()) == set(test_data.keys())
    assert set(iterable.items()) == set(test_data.items())
    assert set(iterable.values()) == set(test_data.values())

def test_iterable_clear(iterable):
    """Test clearing the dictionary."""
    iterable['key'] = 'value'
    iterable.clear()
    assert len(iterable) == 0
    assert 'key' not in iterable

def test_iterable_list_init(iterable_list):
    """Test initialization of IterableList."""
    assert len(iterable_list) == 0
    assert str(iterable_list) == '[]'
    assert repr(iterable_list) == 'IterableList([])'

def test_iterable_list_setitem_getitem(iterable_list):
    """Test setting and getting items."""
    iterable_list[0] = 'first'
    assert iterable_list[0] == 'first'
    
    # Test setting item at specific index
    iterable_list[1] = 'second'
    assert iterable_list[1] == 'second'
    
    # Test setting item at distant index
    iterable_list[5] = 'sixth'
    assert iterable_list[5] == 'sixth'
    # Check that intermediate values are None
    assert iterable_list[2] is None
    
    # Test negative indices
    assert iterable_list[-1] == 'sixth'

def test_iterable_list_contains(iterable_list):
    """Test membership testing."""
    iterable_list[0] = 'value'
    assert 'value' in iterable_list
    assert 'nonexistent' not in iterable_list

def test_iterable_list_len(iterable_list):
    """Test length calculation."""
    assert len(iterable_list) == 0
    iterable_list[0] = 'first'
    iterable_list[1] = 'second'
    assert len(iterable_list) == 2

def test_iterable_list_iter(iterable_list):
    """Test iteration."""
    test_data = ['first', 'second', 'third']
    for i, value in enumerate(test_data):
        iterable_list[i] = value
    
    # Test that we can iterate over values
    assert list(iterable_list) == test_data

def test_iterable_list_index(iterable_list):
    """Test index method."""
    test_data = ['first', 'second', 'third']
    for i, value in enumerate(test_data):
        iterable_list[i] = value
    
    assert iterable_list.index('second') == 1
    with pytest.raises(ValueError):
        iterable_list.index('nonexistent')

def test_iterable_list_append_extend(iterable_list):
    """Test append and extend methods."""
    # Test append
    iterable_list.append('first')
    assert iterable_list[0] == 'first'
    
    # Test extend
    iterable_list.extend(['second', 'third'])
    assert len(iterable_list) == 3
    assert iterable_list[1] == 'second'
    assert iterable_list[2] == 'third'

def test_iterable_list_insert(iterable_list):
    """Test insert method."""
    iterable_list.append('first')
    iterable_list.append('third')
    iterable_list.insert(1, 'second')
    
    assert list(iterable_list) == ['first', 'second', 'third']

def test_iterable_list_remove_pop(iterable_list):
    """Test remove and pop methods."""
    test_data = ['first', 'second', 'third']
    for value in test_data:
        iterable_list.append(value)
    
    # Test pop
    assert iterable_list.pop() == 'third'
    assert len(iterable_list) == 2
    
    # Test remove
    iterable_list.remove('first')
    assert list(iterable_list) == ['second']
    
    with pytest.raises(ValueError):
        iterable_list.remove('nonexistent')

def test_iterable_list_clear(iterable_list):
    """Test clear method."""
    iterable_list.extend(['first', 'second', 'third'])
    iterable_list.clear()
    assert len(iterable_list) == 0
    assert list(iterable_list) == [] 