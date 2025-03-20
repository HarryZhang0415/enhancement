from src.enhancement.cache_result import cache_result

# Test function counter to verify caching
call_count = 0

@cache_result
def expensive_function(x, y=0):
    """Sample function to test caching behavior."""
    global call_count
    call_count += 1
    return x + y

def test_basic_caching():
    """Test basic caching functionality."""
    global call_count
    call_count = 0
    
    # First call should increment counter
    assert expensive_function(1) == 1
    assert call_count == 1
    
    # Second call with same args should use cache
    assert expensive_function(1) == 1
    assert call_count == 1  # Counter shouldn't increment

def test_different_args():
    """Test that different arguments result in different cache entries."""
    global call_count
    call_count = 0
    expensive_function.reset_cache()  # Reset the cache before testing
    
    assert expensive_function(1) == 1
    assert expensive_function(2) == 2
    assert call_count == 2  # Should be called twice for different args

def test_keyword_args():
    """Test caching with keyword arguments."""
    global call_count
    call_count = 0
    expensive_function.reset_cache()
    
    # These should all use the same cache entry
    assert expensive_function(1, y=2) == 3
    assert expensive_function(1, y=2) == 3
    assert expensive_function(x=1, y=2) == 3
    assert call_count == 1

def test_reset_cache():
    """Test cache reset functionality."""
    global call_count
    call_count = 0
    
    assert expensive_function(1) == 1
    assert call_count == 1
    
    expensive_function.reset_cache()
    
    assert expensive_function(1) == 1
    assert call_count == 2  # Should be called again after reset

@cache_result
def function_with_unhashable(lst):
    """Function that takes an unhashable argument (list)."""
    global call_count
    call_count += 1
    return sum(lst)

def test_unhashable_args():
    """Test behavior with unhashable arguments."""
    global call_count
    call_count = 0
    
    # Lists are unhashable, should fall back to direct execution
    assert function_with_unhashable([1, 2, 3]) == 6
    assert function_with_unhashable([1, 2, 3]) == 6
    assert call_count == 2  # Should be called twice as caching is bypassed 