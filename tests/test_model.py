# tests/test_model.py
import pytest
import pandas as pd
import json
import os
from app.main import load_model_from_gcs, load_columns_and_labels, preprocess_features
from app.main import PenguinFeatures, Island, Sex

class TestModelPrediction:
    """Test XGBoost model with known penguin data"""
    
    def setup_method(self):
        """Load model and metadata for testing"""
        self.model = load_model_from_gcs()
        self.expected_columns, self.label_classes = load_columns_and_labels()
    
    def test_model_prediction_adelie(self):
        """Test model prediction for Adelie penguin"""
        # Known Adelie penguin data
        features = PenguinFeatures(
            bill_length_mm=39.1,
            bill_depth_mm=18.7,
            flipper_length_mm=181,
            body_mass_g=3750,
            year=2007,
            sex=Sex.Male,
            island=Island.Torgersen
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        prediction = self.model.predict(X_input.values)[0]
        predicted_label = self.label_classes[int(prediction)]
        
        # Validate prediction structure
        assert isinstance(predicted_label, str)
        assert predicted_label in ["Adelie", "Chinstrap", "Gentoo"]
        
    def test_model_prediction_chinstrap(self):
        """Test model prediction for Chinstrap penguin"""
        # Known Chinstrap penguin data
        features = PenguinFeatures(
            bill_length_mm=46.5,
            bill_depth_mm=17.9,
            flipper_length_mm=192,
            body_mass_g=3500,
            year=2007,
            sex=Sex.Female,
            island=Island.Dream
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        prediction = self.model.predict(X_input.values)[0]
        predicted_label = self.label_classes[int(prediction)]
        
        assert isinstance(predicted_label, str)
        assert predicted_label in ["Adelie", "Chinstrap", "Gentoo"]
        
    def test_model_prediction_gentoo(self):
        """Test model prediction for Gentoo penguin"""
        # Known Gentoo penguin data
        features = PenguinFeatures(
            bill_length_mm=46.1,
            bill_depth_mm=13.2,
            flipper_length_mm=211,
            body_mass_g=4500,
            year=2007,
            sex=Sex.Male,
            island=Island.Biscoe
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        prediction = self.model.predict(X_input.values)[0]
        predicted_label = self.label_classes[int(prediction)]
        
        assert isinstance(predicted_label, str)
        assert predicted_label in ["Adelie", "Chinstrap", "Gentoo"]
        
    def test_model_prediction_consistency(self):
        """Test that model predictions are consistent"""
        features = PenguinFeatures(
            bill_length_mm=39.1,
            bill_depth_mm=18.7,
            flipper_length_mm=181,
            body_mass_g=3750,
            year=2007,
            sex=Sex.Male,
            island=Island.Torgersen
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        
        # Make multiple predictions with same input
        pred1 = self.model.predict(X_input.values)[0]
        pred2 = self.model.predict(X_input.values)[0]
        
        # Should be consistent
        assert pred1 == pred2
        
    def test_model_output_format(self):
        """Test that model output is in expected format"""
        features = PenguinFeatures(
            bill_length_mm=39.1,
            bill_depth_mm=18.7,
            flipper_length_mm=181,
            body_mass_g=3750,
            year=2007,
            sex=Sex.Male,
            island=Island.Torgersen
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        prediction = self.model.predict(X_input.values)
        
        # Check prediction array format
        assert isinstance(prediction, (list, tuple)) or hasattr(prediction, '__iter__')
        assert len(prediction) == 1  # Single prediction
        assert isinstance(int(prediction[0]), int)  # Can convert to int
        
    def test_preprocessing_function(self):
        """Test the preprocessing function works correctly"""
        features = PenguinFeatures(
            bill_length_mm=39.1,
            bill_depth_mm=18.7,
            flipper_length_mm=181,
            body_mass_g=3750,
            year=2007,
            sex=Sex.Male,
            island=Island.Torgersen
        )
        
        X_input = preprocess_features(features, self.expected_columns)
        
        # Check DataFrame structure
        assert isinstance(X_input, pd.DataFrame)
        assert X_input.shape[0] == 1  # Single row
        assert X_input.shape[1] == len(self.expected_columns)  # Correct number of columns
        assert list(X_input.columns) == self.expected_columns  # Correct column order
