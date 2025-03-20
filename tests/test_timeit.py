import pytest
import time
from unittest.mock import MagicMock
from enhancement.timeit import TimeIt

def test_basic_timing():
    """Test basic timing functionality without any callbacks."""
    with TimeIt() as timer:
        time.sleep(0.1)
    
    assert timer.time_elapsed >= 0.1
    assert timer.time_elapsed < 0.15  # Allow some overhead

def test_custom_callbacks():
    """Test TimeIt with custom enter and exit callbacks."""
    enter_called = False
    exit_time = None

    def on_enter():
        nonlocal enter_called
        enter_called = True

    def on_exit(t):
        nonlocal exit_time
        exit_time = t

    with TimeIt(on_enter=on_enter, on_exit=on_exit):
        time.sleep(0.1)

    assert enter_called
    assert exit_time is not None
    assert exit_time >= 0.1
    assert exit_time < 0.15

def test_logger_integration():
    """Test TimeIt with a mock logger."""
    mock_logger = MagicMock()
    
    with TimeIt(logger=mock_logger, tag="TestOperation", level="DEBUG"):
        time.sleep(0.1)

    # Check that logger was called with correct messages
    assert mock_logger.log.call_count == 2
    
    # Check enter log
    enter_call = mock_logger.log.call_args_list[0]
    assert "Starting <TestOperation>" in enter_call[0][0]
    assert enter_call[1]["level_string"] == "DEBUG"
    
    # Check exit log
    exit_call = mock_logger.log.call_args_list[1]
    assert "<TestOperation> took" in exit_call[0][0]
    assert "seconds" in exit_call[0][0]
    assert exit_call[1]["level_string"] == "DEBUG"

def test_print_output(capsys):
    """Test TimeIt with print output when no logger is provided."""
    with TimeIt(tag="PrintTest"):
        time.sleep(0.1)
    
    captured = capsys.readouterr()
    assert "Starting <PrintTest>" in captured.out
    assert "<PrintTest> took" in captured.out
    assert "seconds" in captured.out

def test_error_handling():
    """Test error cases and validation."""
    # Test invalid on_enter
    with pytest.raises(TypeError):
        TimeIt(on_enter="not_callable")

    # Test invalid on_exit
    with pytest.raises(TypeError):
        TimeIt(on_exit="not_callable")

    # Test on_enter with wrong number of arguments
    with pytest.raises(ValueError):
        TimeIt(on_enter=lambda x: None)

    # Test on_exit with wrong number of arguments
    with pytest.raises(ValueError):
        TimeIt(on_exit=lambda: None)

    # Test invalid level type
    with pytest.raises(TypeError):
        TimeIt(tag="test", level=123)

def test_exception_handling():
    """Test that exceptions are properly propagated."""
    enter_called = False
    exit_called = False

    def on_enter():
        nonlocal enter_called
        enter_called = True

    def on_exit(t):
        nonlocal exit_called
        exit_called = True

    with pytest.raises(ValueError):
        with TimeIt(on_enter=on_enter, on_exit=on_exit):
            raise ValueError("Test exception")

    assert enter_called  # Enter should still be called
    assert exit_called  # Exit should still be called

def test_no_callbacks():
    """Test TimeIt without any callbacks or logging."""
    with TimeIt() as timer:
        time.sleep(0.1)
    
    assert timer.time_elapsed >= 0.1
    assert timer.time_elapsed < 0.15

def test_level_case_sensitivity():
    """Test that log level is properly converted to uppercase."""
    mock_logger = MagicMock()
    
    with TimeIt(logger=mock_logger, tag="TestOperation", level="debug"):
        pass

    assert mock_logger.log.call_args[1]["level_string"] == "DEBUG"

def test_tag_without_logger():
    """Test that tag works with print when no logger is provided."""
    with pytest.raises(TypeError):
        # Should raise TypeError for invalid level type
        TimeIt(tag="test", level=None)

    # Should work fine with string level
    with TimeIt(tag="test", level="INFO") as timer:
        time.sleep(0.1)
    
    assert timer.time_elapsed is not None 