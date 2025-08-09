# tests/test_edge_cases.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestEdgeCases:
    """Test boundary conditions (e.g., extreme values, empty requests)"""
    
    def test_empty_request(self):
        """Test completely empty request"""
        response = client.post("/predict", json={})
        assert response.status_code == 422
    
    def test_negative_bill_length_mm(self):
        """Test negative bill_length_mm"""
        sample_data = {
            "bill_length_mm": -10.0,  # Negative value
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200  # Model should handle gracefully
        assert "prediction" in response.json()
    
    def test_negative_bill_depth_mm(self):
        """Test negative bill_depth_mm"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": -5.0,  # Negative value
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_negative_flipper_length_mm(self):
        """Test negative flipper_length_mm"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": -100,  # Negative value
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_negative_body_mass_g(self):
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
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_zero_values(self):
        """Test zero values for all measurements"""
        sample_data = {
            "bill_length_mm": 0.0,
            "bill_depth_mm": 0.0,
            "flipper_length_mm": 0,
            "body_mass_g": 0,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_extremely_large_values(self):
        """Test extremely large values"""
        sample_data = {
            "bill_length_mm": 9999.9,  # Extremely large
            "bill_depth_mm": 9999.9,   # Extremely large
            "flipper_length_mm": 9999,
            "body_mass_g": 999999,     # Extremely large
            "year": 2007,
            "sex": "female",
            "island": "Biscoe"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_very_small_positive_values(self):
        """Test very small positive values"""
        sample_data = {
            "bill_length_mm": 0.001,   # Very small
            "bill_depth_mm": 0.001,    # Very small
            "flipper_length_mm": 1,
            "body_mass_g": 1,
            "year": 2007,
            "sex": "female",
            "island": "Dream"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_boundary_year_values(self):
        """Test boundary year values"""
        sample_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 1900,  # Very old year
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
        
        # Test future year
        sample_data["year"] = 3000  # Future year
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_float_precision_edge_cases(self):
        """Test floating point precision edge cases"""
        sample_data = {
            "bill_length_mm": 39.123456789123456789,  # High precision
            "bill_depth_mm": 18.700000000000001,      # Floating point precision
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        assert "prediction" in response.json()
    
    def test_all_valid_enum_combinations(self):
        """Test all valid combinations of sex and island enums"""
        base_data = {
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007
        }
        
        sex_values = ["male", "female"]
        island_values = ["Torgersen", "Biscoe", "Dream"]
        
        for sex in sex_values:
            for island in island_values:
                sample_data = base_data.copy()
                sample_data["sex"] = sex
                sample_data["island"] = island
                
                response = client.post("/predict", json=sample_data)
                assert response.status_code == 200
                assert "prediction" in response.json()
    
    def test_malformed_json(self):
        """Test malformed JSON - this tests the FastAPI framework handling"""
        # Note: This test verifies framework behavior, not our application logic
        response = client.post(
            "/predict", 
            content="{'invalid': 'json'",  # Malformed JSON
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
