import pytest
from src.enhancement.graph import DiddleScope, GraphObject, Vertex

def test_basic_diddle(basic_graph_object):
    """Test basic diddle functionality"""
    # Check initial value
    assert basic_graph_object.value() == 42
    
    # Use diddle scope to temporarily change value
    with DiddleScope():
        basic_graph_object.value.set_diddle(10)
        assert basic_graph_object.value() == 10
        assert basic_graph_object.double_value() == 20
    
    # Check value returns to normal after scope exit
    assert basic_graph_object.value() == 42
    assert basic_graph_object.double_value() == 84

def test_nested_diddle_scopes(basic_graph_object):
    """Test nested diddle scopes"""
    assert basic_graph_object.value() == 42
    
    with DiddleScope():
        basic_graph_object.value.set_diddle(10)
        assert basic_graph_object.value() == 10
        
        with DiddleScope():
            basic_graph_object.value.set_diddle(20)
            assert basic_graph_object.value() == 20
        
        # Should return to outer scope value
        assert basic_graph_object.value() == 10
    
    # Should return to original value
    assert basic_graph_object.value() == 42

def test_diddle_with_fixed_values(basic_graph_object):
    """Test interaction between diddles and fixed values"""
    # Set a fixed value
    basic_graph_object.value.set_value(30)
    assert basic_graph_object.value() == 30
    
    # Diddle should temporarily override fixed value
    with DiddleScope():
        basic_graph_object.value.set_diddle(10)
        assert basic_graph_object.value() == 10
    
    # Should return to fixed value
    assert basic_graph_object.value() == 30

def test_clear_diddle(basic_graph_object):
    """Test clearing diddle values"""
    with DiddleScope():
        basic_graph_object.value.set_diddle(10)
        assert basic_graph_object.value() == 10
        
        basic_graph_object.value.clear_diddle()
        assert basic_graph_object.value() == 42

def test_diddle_dependencies(basic_graph_object):
    """Test that diddles properly update dependent vertices"""
    with DiddleScope():
        # Set diddle and verify dependent values update
        basic_graph_object.value.set_diddle(10)
        assert basic_graph_object.value() == 10
        assert basic_graph_object.double_value() == 20
        assert basic_graph_object.triple_value() == 30
        
        # Clear diddle and verify dependent values return to normal
        basic_graph_object.value.clear_diddle()
        assert basic_graph_object.value() == 42
        assert basic_graph_object.double_value() == 84
        assert basic_graph_object.triple_value() == 126

def test_diddle_debug_mode():
    """Test diddle scope with debug mode"""
    class DebugExample(GraphObject):
        @Vertex
        def value(self):
            return 42
    
    obj = DebugExample()
    
    # Use diddle scope with debug mode enabled
    with DiddleScope(debug_mode=True):
        obj.value.set_diddle(10)
        assert obj.value() == 10
    
    assert obj.value() == 42 