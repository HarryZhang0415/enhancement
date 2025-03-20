import pytest
from enhancement import get_safe, get_safe_object

@pytest.fixture
def test_dict():
    return {
        'string_key': 'value',
        'int_key': 42,
        'bool_key': True,
        'false_key': False,
        'zero_key': 0,
        'empty_string_key': '',
        'none_key': None,
        'list_key': [1, 2, 3],
        'dict_key': {'nested': 'value'}
    }

def test_get_safe_existing_keys(test_dict):
    """Test get_safe with existing keys"""
    assert get_safe(test_dict, 'string_key', 'default') == 'value'
    assert get_safe(test_dict, 'int_key', 0) == 42
    assert get_safe(test_dict, 'bool_key', False) == True
    assert get_safe(test_dict, 'list_key', []) == [1, 2, 3]

def test_get_safe_falsy_values(test_dict):
    """Test get_safe with falsy values to ensure they're returned correctly"""
    assert get_safe(test_dict, 'false_key', True) == False
    assert get_safe(test_dict, 'zero_key', 1) == 0
    assert get_safe(test_dict, 'empty_string_key', 'default') == ''

def test_get_safe_missing_keys(test_dict):
    """Test get_safe with missing keys"""
    assert get_safe(test_dict, 'non_existent', 'default') == 'default'
    assert get_safe(test_dict, 'missing_int', 42) == 42
    assert get_safe(test_dict, 'missing_list', [1]) == [1]

def test_get_safe_none_values(test_dict):
    """Test get_safe with None values"""
    assert get_safe(test_dict, 'none_key', 'default') == 'default'
    assert get_safe(test_dict, 'non_existent', None) == None

class TestObject:
    def __init__(self):
        self.string_attr = 'value'
        self.int_attr = 42
        self.bool_attr = True
        self.false_attr = False
        self.zero_attr = 0
        self.empty_string_attr = ''
        self.none_attr = None
        self.list_attr = [1, 2, 3]

@pytest.fixture
def test_obj():
    return TestObject()

def test_get_safe_object_existing_attributes(test_obj):
    """Test get_safe_object with existing attributes"""
    assert get_safe_object(test_obj, 'string_attr', 'default') == 'value'
    assert get_safe_object(test_obj, 'int_attr', 0) == 42
    assert get_safe_object(test_obj, 'bool_attr', False) == True
    assert get_safe_object(test_obj, 'list_attr', []) == [1, 2, 3]

def test_get_safe_object_falsy_values(test_obj):
    """Test get_safe_object with falsy values"""
    assert get_safe_object(test_obj, 'false_attr', True) == False
    assert get_safe_object(test_obj, 'zero_attr', 1) == 0
    assert get_safe_object(test_obj, 'empty_string_attr', 'default') == ''

def test_get_safe_object_missing_attributes(test_obj):
    """Test get_safe_object with missing attributes"""
    assert get_safe_object(test_obj, 'non_existent', 'default') == 'default'
    assert get_safe_object(test_obj, 'missing_int', 42) == 42
    assert get_safe_object(test_obj, 'missing_list', [1]) == [1]

def test_get_safe_object_none_values(test_obj):
    """Test get_safe_object with None values"""
    assert get_safe_object(test_obj, 'none_attr', 'default') == None
    assert get_safe_object(test_obj, 'non_existent', None) == None 