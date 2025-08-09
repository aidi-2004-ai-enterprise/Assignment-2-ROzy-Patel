# tests/test_validation.py
import pytest
from fastapi.testclient import TestClient
from app.main import app, PenguinFeatures, Island, Sex
from pydantic import ValidationError

client = TestClient(app)

class TestInputValidation:
    """Handle missing or invalid inputs gracefully"""
    
    def test_missing_bill_length_mm(self):
        """Test for missing bill_length_mm field"""
        sample_data = {
            # "bill_length_mm": 39.1,  # Missing
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "bill_length_mm" in str(response.json())
    
    def test_missing_bill_depth_mm(self):
        """Test for missing bill_depth_mm field"""
        sample_data = {
            "bill_length_mm": 39.1,
            # "bill_depth_mm": 18.7,  # Missing
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "bill_depth_mm" in str(response.json())
    
    def test_missing_flipper_length_mm(self):
        """Test for missing flipper_length_mm field"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            # "flipper_length_mm": 181,  # Missing
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "flipper_length_mm" in str(response.json())
    
    def test_missing_body_mass_g(self):
        """Test for missing body_mass_g field"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            # "body_mass_g": 3750,  # Missing
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "body_mass_g" in str(response.json())
    
    def test_missing_year(self):
        """Test for missing year field"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            # "year": 2007,  # Missing
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "year" in str(response.json())
    
    def test_missing_sex(self):
        """Test for missing sex field"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            # "sex": "male",  # Missing
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "sex" in str(response.json())
    
    def test_missing_island(self):
        """Test for missing island field"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male"
            # "island": "Torgersen"  # Missing
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "island" in str(response.json())
    
    def test_invalid_sex_value(self):
        """Test for invalid sex value"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "invalid_sex",  # Invalid value
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "sex" in str(response.json())
    
    def test_invalid_island_value(self):
        """Test for invalid island value"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "invalid_island"  # Invalid value
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
        assert "island" in str(response.json())

class TestInvalidDataTypes:
    """Test for invalid data types (e.g., strings instead of floats)"""
    
    def test_string_bill_length_mm(self):
        """Test string instead of float for bill_length_mm"""
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
    
    def test_string_bill_depth_mm(self):
        """Test string instead of float for bill_depth_mm"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": "not_a_number",  # String instead of float
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
    
    def test_string_flipper_length_mm(self):
        """Test string instead of float for flipper_length_mm"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": "not_a_number",  # String instead of float
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
    
    def test_string_body_mass_g(self):
        """Test string instead of float for body_mass_g"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": "not_a_number",  # String instead of float
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
    
    def test_string_year(self):
        """Test string instead of int for year"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": "not_a_number",  # String instead of int
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
    
    def test_null_values(self):
        """Test null values"""
        sample_data = {
            "bill_length_mm": None,  # Null value
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 422
