import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), '..')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j driver for testing without actual database connection."""
    mock_driver = Mock()
    mock_session = Mock()
    mock_result = Mock()
    mock_result.single.return_value = {"count": 1}
    mock_session.run.return_value = mock_result

    # Create a mock session context manager
    mock_session_context = Mock()
    mock_session_context.__enter__ = Mock(return_value=mock_session)
    mock_session_context.__exit__ = Mock(return_value=None)
    mock_driver.session.return_value = mock_session_context

    return mock_driver

@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    return mock_redis

@pytest.fixture(autouse=True)
def mock_dependencies(mock_neo4j_driver, mock_redis):
    """Automatically mock Neo4j and Redis dependencies for all tests."""
    with patch('app.core.neo4j.get_neo4j_driver', return_value=mock_neo4j_driver), \
         patch('app.core.deps.get_redis_client', return_value=mock_redis):
        yield
