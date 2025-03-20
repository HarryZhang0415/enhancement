import pytest
import threading
from concurrent.futures import ThreadPoolExecutor
from enhancement.singleton import Singleton

class TestClass(metaclass=Singleton):
    def __init__(self, value: str = "default"):
        self.value = value

class AnotherTestClass(metaclass=Singleton):
    def __init__(self, value: str = "default"):
        self.value = value

@pytest.fixture(autouse=True)
def reset_singletons():
    # Reset all instances before each test
    Singleton.reset()
    yield

def test_singleton_instance_uniqueness():
    """Test that multiple instantiations return the same instance."""
    instance1 = TestClass()
    instance2 = TestClass()
    assert instance1 is instance2

def test_different_classes_different_instances():
    """Test that different classes have different singleton instances."""
    test_instance = TestClass()
    another_instance = AnotherTestClass()
    assert test_instance is not another_instance

def test_constructor_args_first_only():
    """Test that only the first constructor call's arguments are used."""
    first = TestClass("first")
    second = TestClass("second")
    assert first.value == "first"
    assert second.value == "first"

def test_reset_specific_class():
    """Test resetting a specific class instance."""
    original = TestClass("original")
    Singleton.reset(TestClass)
    new = TestClass("new")
    assert original.value != new.value
    assert new.value == "new"

def test_reset_all():
    """Test resetting all singleton instances."""
    test_instance = TestClass()
    another_instance = AnotherTestClass()
    Singleton.reset()
    new_test = TestClass()
    new_another = AnotherTestClass()
    assert test_instance is not new_test
    assert another_instance is not new_another

def test_thread_safety():
    """Test thread-safe instance creation."""
    def create_instance():
        return TestClass()

    # Create instances from multiple threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_instance) for _ in range(20)]
        instances = [future.result() for future in futures]

    # Verify all instances are the same
    first_instance = instances[0]
    for instance in instances[1:]:
        assert first_instance is instance

def test_concurrent_reset_and_create():
    """Test concurrent reset and instance creation."""
    def worker():
        for _ in range(10):
            instance = TestClass()
            assert isinstance(instance, TestClass)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    reset_thread = threading.Thread(target=lambda: [Singleton.reset() for _ in range(5)])

    # Start all threads
    for thread in threads:
        thread.start()
    reset_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    reset_thread.join() 