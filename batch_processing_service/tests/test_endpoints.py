import pytest
import json
from app import create_app, task_queue

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    # Ensure tasks don't actually run during tests
    task_queue.is_async = False
    
    yield app
    
    # Cleanup: Clear any queued jobs
    task_queue.empty()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

class TestEndpoints:
    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        
        # Check response
        assert response.status_code == 200
        assert response.json["status"] == "healthy"
    
    def test_enqueue_data_job(self, client):
        """Test enqueueing a data processing job"""
        payload = {
            "job_type": "data_processing",
            "data": {
                "test_key": "test_value"
            },
            "options": {
                "use_ray": False
            }
        }
        
        response = client.post(
            '/enqueue',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 202
        assert "job_id" in response.json
        assert response.json["status"] == "queued"
    
    def test_enqueue_text_job(self, client):
        """Test enqueueing a text processing job"""
        payload = {
            "job_type": "text_processing",
            "data": "This is test text for processing",
            "options": {
                "operations": ["count", "tokenize"],
                "use_ray": False
            }
        }
        
        response = client.post(
            '/enqueue',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 202
        assert "job_id" in response.json
        assert response.json["status"] == "queued"
    
    def test_invalid_job_type(self, client):
        """Test sending an invalid job type"""
        payload = {
            "job_type": "invalid_type",
            "data": "test data"
        }
        
        response = client.post(
            '/enqueue',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 400
        assert "error" in response.json
    
    def test_missing_required_fields(self, client):
        """Test sending request with missing required fields"""
        # Missing job_type
        payload = {
            "data": "test data"
        }
        
        response = client.post(
            '/enqueue',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 400
        assert "error" in response.json
        
        # Missing data
        payload = {
            "job_type": "text_processing"
        }
        
        response = client.post(
            '/enqueue',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 400
        assert "error" in response.json
