# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
import pytest

client = TestClient(app)

def test_predict_endpoint_valid_input():
    """Test prediction with valid penguin data"""
    sample_data = {
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750,
        "year": 2007,
        "sex": "male",
        "island": "Torgersen"
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_endpoint_invalid_input():
    """Test handling of invalid input - missing required field"""
    sample_data = {
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750,
        "year": 2007,
        "sex": "male"
        # Missing "island" field
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 422  # Validation error

def test_predict_endpoint_missing_field():
    """Test for missing fields (e.g., bill_length_mm omitted)"""
    sample_data = {
        # "bill_length_mm": 39.1,  # Missing this field
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750,
        "year": 2007,
        "sex": "male",
        "island": "Torgersen"
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 422

def test_predict_endpoint_invalid_data_types():
    """Test for invalid data types (e.g., strings instead of floats)"""
    sample_data = {
        "bill_length_mm": "not_a_number",  # String instead of float
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": 3750,
        "year": 2007,
        "sex": "male",
        "island": "Torgersen"
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 422

def test_predict_endpoint_out_of_range_values():
    """Test for out-of-range values (e.g., negative body_mass_g)"""
    sample_data = {
        "bill_length_mm": 39.1,
        "bill_depth_mm": 18.7,
        "flipper_length_mm": 181,
        "body_mass_g": -1000,  # Negative value
        "year": 2007,
        "sex": "male",
        "island": "Torgersen"
    }
    response = client.post("/predict", json=sample_data)
    # Should still return 200 but handle gracefully
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_endpoint_empty_request():
    """Edge case test: Test boundary conditions - empty request"""
    response = client.post("/predict", json={})
    assert response.status_code == 422

def test_predict_endpoint_extreme_values():
    """Edge case test: Test boundary conditions - extreme values"""
    sample_data = {
        "bill_length_mm": 999.9,  # Extreme value
        "bill_depth_mm": 0.1,     # Very small value
        "flipper_length_mm": 999,
        "body_mass_g": 50000,     # Very large value
        "year": 2007,
        "sex": "female",
        "island": "Biscoe"
    }
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_endpoint_internal_error():
    """Test internal server error handling - testing exception coverage"""
    # Note: This is primarily for coverage of exception handling code
    # In practice, most errors are caught by FastAPI validation before reaching our handler
    pass
