import pytest
from src.enhancement.graph import CLEAR

def test_vertex_basic_value(basic_graph_object):
    """Test basic vertex value computation"""
    assert basic_graph_object.value() == 42
    assert basic_graph_object.double_value() == 84
    assert basic_graph_object.triple_value() == 126

def test_vertex_caching(complex_graph_object):
    """Test that vertex values are properly cached"""
    # First call increments counter to 1
    assert complex_graph_object.counter() == 1
    # Second call should return cached value
    assert complex_graph_object.counter() == 1
    # Dependent calculations should use cached value
    assert complex_graph_object.squared() == 1
    assert complex_graph_object.cubed() == 1
    # Counter should still be 1 due to caching
    assert complex_graph_object.counter() == 1

def test_vertex_set_value(basic_graph_object):
    """Test setting fixed values on vertices"""
    # Set a new fixed value
    basic_graph_object.value.set_value(10)
    assert basic_graph_object.value() == 10
    # Check that dependent values are updated
    assert basic_graph_object.double_value() == 20
    assert basic_graph_object.triple_value() == 30

def test_vertex_clear_value(basic_graph_object):
    """Test clearing fixed values"""
    # Set and verify fixed value
    basic_graph_object.value.set_value(10)
    assert basic_graph_object.value() == 10
    
    # Clear the value
    basic_graph_object.value.clear_value()
    # Should return to original computed value
    assert basic_graph_object.value() == 42

def test_vertex_is_fixed(basic_graph_object):
    """Test checking if vertex has fixed value"""
    assert not basic_graph_object.value.is_fixed()
    basic_graph_object.value.set_value(10)
    assert basic_graph_object.value.is_fixed()
    basic_graph_object.value.clear_value()
    assert not basic_graph_object.value.is_fixed()

def test_vertex_dependencies(basic_graph_object):
    """Test that changing a value updates dependent vertices"""
    # Get initial values to establish dependencies
    initial_double = basic_graph_object.double_value()
    initial_triple = basic_graph_object.triple_value()
    
    # Change base value
    basic_graph_object.value.set_value(10)
    
    # Check that dependent values changed
    assert basic_graph_object.double_value() != initial_double
    assert basic_graph_object.triple_value() != initial_triple
    assert basic_graph_object.double_value() == 20
    assert basic_graph_object.triple_value() == 30 