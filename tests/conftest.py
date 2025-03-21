import pytest
from src.enhancement.graph import GraphObject, Vertex, Graph, DiddleScope

@pytest.fixture
def graph():
    return Graph()

@pytest.fixture
def basic_graph_object():
    class BasicExample(GraphObject):
        @Vertex
        def value(self):
            return 42
        
        @Vertex
        def double_value(self):
            return self.value() * 2
        
        @Vertex
        def triple_value(self):
            return self.value() * 3
    
    return BasicExample()

@pytest.fixture
def complex_graph_object():
    class ComplexExample(GraphObject):
        def __init__(self):
            self._counter = 0
            
        @Vertex
        def counter(self):
            self._counter += 1
            return self._counter
            
        @Vertex
        def squared(self):
            return self.counter() ** 2
            
        @Vertex
        def cubed(self):
            return self.counter() ** 3
    
    return ComplexExample() 