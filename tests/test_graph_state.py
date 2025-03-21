import pytest
from src.enhancement.graph import Graph, GraphObject, Vertex
import time

def test_graph_state_stack(graph):
    """Test graph state stack management"""
    initial_state = graph.active_state
    
    # Push a new state
    new_state = type(initial_state)(graph)
    graph.push_state(new_state)
    assert graph.active_state == new_state
    
    # Pop state
    popped = graph.pop_state()
    assert popped == new_state
    assert graph.active_state == initial_state

def test_performance_monitoring():
    """Test performance monitoring functionality"""
    graph = Graph()
    graph._gather_performance = True
    
    class SlowExample(GraphObject):
        @Vertex
        def slow_operation(self):
            time.sleep(0.1)  # Simulate slow operation
            return 42
    
    obj = SlowExample()
    
    # Call the slow operation with explicit timing context
    with graph.time_it(obj.slow_operation):
        result = obj.slow_operation()
    
    assert result == 42
    
    # Check that timing was recorded for the vertex
    assert obj.slow_operation in graph.timings
    assert len(graph.timings[obj.slow_operation]) > 0
    assert graph.timings[obj.slow_operation][0] >= 0.1  # Should be at least our sleep time
    
    # Reset timings
    graph.reset_timings()
    assert len(graph.timings) == 0

def test_thread_safety():
    """Test thread-safe state management"""
    import threading
    
    class ThreadExample(GraphObject):
        @Vertex
        def value(self):
            return threading.current_thread().name
    
    obj = ThreadExample()
    results = []
    
    def thread_func():
        results.append(obj.value())
    
    # Create and run threads
    threads = [
        threading.Thread(target=thread_func, name=f"Thread-{i}")
        for i in range(3)
    ]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Verify each thread got its own value
    assert len(results) == 3
    assert len(set(results)) == 3  # All values should be unique

def test_graph_debug_mode(graph):
    """Test debug mode functionality"""
    class DebugExample(GraphObject):
        @Vertex
        def value(self):
            return 42
    
    obj = DebugExample()
    
    # Enable debug mode
    graph._debug_mode = True
    assert graph.is_debug_mode
    
    # Call vertex (output would be printed in debug mode)
    result = obj.value()
    assert result == 42

def test_graph_state_copy():
    """Test graph state copying functionality"""
    class Example(GraphObject):
        @Vertex
        def value(self):
            return 42
    
    obj = Example()
    graph = Graph()
    
    # Get initial state
    initial_state = graph.active_state
    
    # Set a value in initial state
    obj.value()
    
    # Create and copy to new state
    new_state = type(initial_state)(graph)
    initial_state.copy(new_state)
    
    # Verify copy has same values
    assert len(new_state) == len(initial_state)
    for key in initial_state:
        assert key in new_state

def test_graph_calculation_state():
    """Test graph calculation state tracking"""
    class Example(GraphObject):
        @Vertex
        def value(self):
            return 42
        
        @Vertex
        def dependent(self):
            return self.value() * 2
    
    obj = Example()
    graph = Graph()
    
    # Initially not calculating
    assert not graph.is_calculating()
    
    # During calculation
    result = obj.dependent()  # This will trigger calculation
    assert result == 84  # Verify result 