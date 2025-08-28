from fastapi.testclient import TestClient

def test_client(client):
    """Test the TestClient fixture."""
    assert type(client) == TestClient