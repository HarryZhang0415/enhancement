import pytest
from enhancement.graph import (
    Graph, GraphObject, Vertex, DiddleScope, SetScope,
    is_fixed, _graph
)

# Test fixtures
class SimpleGraph(GraphObject):
    @Vertex
    def a(self):
        return 5

    @Vertex
    def b(self):
        return self.a() * 2

    @Vertex
    def c(self):
        return self.b() + 3

class DependentGraph(GraphObject):
    def __init__(self, other_graph):
        super(DependentGraph, self).__init__()
        self.other = other_graph

    @Vertex
    def x(self):
        return self.other.a() * 3

    @Vertex
    def y(self):
        return self.x() + self.other.b()

@pytest.fixture
def simple_graph():
    return SimpleGraph()

@pytest.fixture
def dependent_graph(simple_graph):
    return DependentGraph(simple_graph)

@pytest.fixture
def graph():
    return Graph()

# Test topological sort
def test_topological_sort(simple_graph):
    simple_graph.c()  # Build dependencies
    sorted_nodes = _graph.get_topological_sort()
    assert len(sorted_nodes) == 3
    # Verify order: a should come before b, b should come before c
    a_idx = sorted_nodes.index('SimpleGraph.a')
    b_idx = sorted_nodes.index('SimpleGraph.b')
    c_idx = sorted_nodes.index('SimpleGraph.c')
    assert a_idx < b_idx < c_idx

# Test basic vertex evaluation
def test_basic_vertex_evaluation(simple_graph):
    assert simple_graph.a() == 5
    assert simple_graph.b() == 10
    assert simple_graph.c() == 13

# Test dependency tracking
def test_dependency_tracking(simple_graph):
    # First evaluation to build dependencies
    simple_graph.c()
    
    # Verify dependencies through NetworkX graph
    nx_graph = _graph.to_networkx()
    assert 'SimpleGraph.a' in nx_graph
    assert 'SimpleGraph.b' in nx_graph
    assert 'SimpleGraph.c' in nx_graph
    
    # Check edges
    assert nx_graph.has_edge('SimpleGraph.a', 'SimpleGraph.b')
    assert nx_graph.has_edge('SimpleGraph.b', 'SimpleGraph.c')

# Test value setting and clearing
def test_value_setting_and_clearing(simple_graph):
    # Set value
    simple_graph.a.set_value(10)
    assert simple_graph.a() == 10
    assert simple_graph.b() == 20
    assert simple_graph.c() == 23

    # Clear value
    simple_graph.a.clear_value()
    assert simple_graph.a() == 5
    assert simple_graph.b() == 10
    assert simple_graph.c() == 13

# Test DiddleScope
def test_diddle_scope(simple_graph):
    original_a = simple_graph.a()
    
    with DiddleScope():
        simple_graph.a.set_diddle(20)
        assert simple_graph.a() == 20
        assert simple_graph.b() == 40
    
    # Values should be back to original after exiting DiddleScope
    assert simple_graph.a() == original_a
    assert simple_graph.b() == original_a * 2

# Test SetScope
def test_set_scope(simple_graph):
    original_a = simple_graph.a()
    
    with SetScope({simple_graph.a: 15}):
        assert simple_graph.a() == 15
        assert simple_graph.b() == 30
    
    # Values should be back to original after exiting SetScope
    assert simple_graph.a() == original_a
    assert simple_graph.b() == original_a * 2

# Test nested graph dependencies
def test_nested_dependencies(simple_graph, dependent_graph):
    assert dependent_graph.x() == 15  # 5 * 3
    assert dependent_graph.y() == 25  # (5 * 3) + (5 * 2)
    
    # Modify base graph value
    simple_graph.a.set_value(10)
    assert dependent_graph.x() == 30  # 10 * 3
    assert dependent_graph.y() == 50  # (10 * 3) + (10 * 2)

# Test cycle detection
def test_cycle_detection(graph):
    class CyclicGraph(GraphObject):
        @Vertex
        def x(self):
            return self.y()

        @Vertex
        def y(self):
            return self.x()
    
    cyclic = CyclicGraph()
    with pytest.raises(RuntimeError):
        cyclic.x()

# Test fixed state checking
def test_is_fixed(simple_graph):
    assert not is_fixed(simple_graph.a)
    simple_graph.a.set_value(10)
    assert is_fixed(simple_graph.a)
    simple_graph.a.clear_value()
    assert not is_fixed(simple_graph.a)

# Test error cases
def test_error_cases(simple_graph):
    # Test setting value during calculation
    class ErrorGraph(GraphObject):
        def __init__(self, sg):
            super(ErrorGraph, self).__init__()
            self.sg = sg

        @Vertex
        def bad_vertex(self):
            self.sg.a.set_value(20)  # This should raise an error
            return 42

    error_graph = ErrorGraph(simple_graph)
    with pytest.raises(RuntimeError):
        error_graph.bad_vertex()

# Test performance tracking
def test_performance_tracking(simple_graph):
    _graph._gather_performance = True
    _graph.reset_timings()
    
    # Perform some operations
    simple_graph.c()
    
    # Check if timings were recorded
    assert len(_graph.timings) > 0
    
    # Reset performance tracking
    _graph._gather_performance = False
    _graph.reset_timings()

# Test debug mode
def test_debug_mode(simple_graph, capsys):
    _graph._debug_mode = True
    simple_graph.c()
    captured = capsys.readouterr()
    assert "SimpleGraph" in captured.out
    _graph._debug_mode = False

# Test graph visualization
def test_graph_visualization(simple_graph):
    # Just test that visualization doesn't raise errors
    simple_graph.c()  # Build some dependencies
    _graph.visualize()

# Test path finding
def test_path_finding(simple_graph):
    simple_graph.c()  # Build dependencies
    paths = _graph.get_all_paths('SimpleGraph.a', 'SimpleGraph.c')
    assert len(paths) == 1
    assert paths[0] == ['SimpleGraph.a', 'SimpleGraph.b', 'SimpleGraph.c'] 