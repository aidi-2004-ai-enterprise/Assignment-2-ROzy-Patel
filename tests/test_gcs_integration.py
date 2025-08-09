# tests/test_gcs_integration.py
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from app.main import load_model_from_gcs, load_columns_and_labels

class TestGCSIntegration:
    """Test Google Cloud Storage integration functionality"""
    
    def test_load_model_from_gcs_success(self):
        """Test successful model loading from GCS"""
        # This test will actually use the real GCS credentials if available
        model = load_model_from_gcs()
        assert model is not None
        # Test that model can make predictions using the expected columns
        columns, _ = load_columns_and_labels()
        import pandas as pd
        # Create test data with all expected columns (9 features)
        test_data = pd.DataFrame([[39.1, 18.7, 181, 3750, 2007, 1, 0, 1, 0]], 
                                columns=columns)
        prediction = model.predict(test_data.values)
        assert len(prediction) == 1

    @patch.dict(os.environ, {}, clear=True)
    @patch('app.main.storage.Client')
    def test_load_model_from_gcs_no_credentials(self, mock_client):
        """Test GCS loading without credentials falls back to local"""
        # Remove GCS environment variables to test fallback
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        
        mock_client.side_effect = Exception("No credentials")
        
        model = load_model_from_gcs()
        assert model is not None  # Should fallback to local model

    @patch('app.main.storage.Client')
    def test_load_model_from_gcs_client_error(self, mock_client):
        """Test GCS client error falls back to local"""
        mock_client.side_effect = Exception("GCS connection failed")
        
        model = load_model_from_gcs()
        assert model is not None  # Should fallback to local model

    @patch('app.main.storage.Client')
    def test_load_model_from_gcs_blob_error(self, mock_client):
        """Test GCS blob download error falls back to local"""
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.download_as_bytes.side_effect = Exception("Blob download failed")
        mock_bucket.blob.return_value = mock_blob
        mock_client.return_value.bucket.return_value = mock_bucket
        
        model = load_model_from_gcs()
        assert model is not None  # Should fallback to local model

    def test_load_columns_and_labels(self):
        """Test loading columns and labels metadata"""
        columns, labels = load_columns_and_labels()
        
        # Check columns
        assert isinstance(columns, list)
        assert len(columns) > 0
        assert 'bill_length_mm' in columns
        assert 'bill_depth_mm' in columns
        
        # Check labels  
        assert isinstance(labels, list)
        assert len(labels) == 3  # Adelie, Chinstrap, Gentoo
        assert 'Adelie' in labels
        assert 'Chinstrap' in labels
        assert 'Gentoo' in labels

    @patch('app.main.open', side_effect=FileNotFoundError("File not found"))
    def test_load_columns_and_labels_file_error(self, mock_open):
        """Test error handling when metadata files are missing"""
        with pytest.raises(FileNotFoundError):
            load_columns_and_labels()
