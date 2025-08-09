import random
from locust import HttpUser, task, between

class PenguinAPIUser(HttpUser):
    """Simulate users making penguin predictions"""
    
    # Wait between 1-3 seconds between requests (realistic user behavior)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts"""
        # Test health endpoint on startup
        self.client.get("/health")
    
    @task(3)
    def predict_adelie(self):
        """Simulate predicting Adelie penguin (most common)"""
        payload = {
            "bill_length_mm": random.uniform(32.1, 46.0),
            "bill_depth_mm": random.uniform(15.5, 21.5),
            "flipper_length_mm": random.uniform(172, 210),
            "body_mass_g": random.uniform(2850, 4775),
            "year": random.choice([2007, 2008, 2009]),
            "sex": random.choice(["male", "female"]),
            "island": random.choice(["Torgersen", "Biscoe", "Dream"])
        }
        
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    response.success()
                else:
                    response.failure("Missing prediction in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def predict_gentoo(self):
        """Simulate predicting Gentoo penguin"""
        payload = {
            "bill_length_mm": random.uniform(40.9, 59.6),
            "bill_depth_mm": random.uniform(13.1, 17.3), 
            "flipper_length_mm": random.uniform(203, 231),
            "body_mass_g": random.uniform(3950, 6300),
            "year": random.choice([2007, 2008, 2009]),
            "sex": random.choice(["male", "female"]),
            "island": "Biscoe"  # Gentoo are mostly on Biscoe
        }
        
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    response.success()
                else:
                    response.failure("Missing prediction in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def predict_chinstrap(self):
        """Simulate predicting Chinstrap penguin"""
        payload = {
            "bill_length_mm": random.uniform(40.9, 58.0),
            "bill_depth_mm": random.uniform(16.4, 20.8),
            "flipper_length_mm": random.uniform(178, 212),
            "body_mass_g": random.uniform(2700, 4800),
            "year": random.choice([2007, 2008, 2009]),
            "sex": random.choice(["male", "female"]),
            "island": "Dream"  # Chinstrap are mostly on Dream
        }
        
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    response.success()
                else:
                    response.failure("Missing prediction in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def health_check(self):
        """Periodic health checks"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "ok":
                    response.success()
                else:
                    response.failure("Health check failed")
            else:
                response.failure(f"Health check returned {response.status_code}")
    
    @task(1)
    def invalid_request(self):
        """Test error handling with invalid requests"""
        invalid_payload = {
            "bill_length_mm": "invalid",  # Should be float
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male",
            "island": "Torgersen"
        }
        
        with self.client.post("/predict", json=invalid_payload, catch_response=True) as response:
            if response.status_code == 422:  # Validation error expected
                response.success()
            else:
                response.failure(f"Expected 422, got {response.status_code}")