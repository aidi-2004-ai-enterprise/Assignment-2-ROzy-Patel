import xgboost as xgb
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import json
import logging
import os
from google.cloud import storage
from dotenv import load_dotenv


# Logging setup
logging.basicConfig(level=logging.INFO)

# Load .env for GCS config
load_dotenv()

# Paths
BASE_PATH = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_PATH, "data", "model.json")
COLUMNS_PATH = os.path.join(BASE_PATH, "data", "columns.json")
LABELS_PATH = os.path.join(BASE_PATH, "data", "label_classes.json")

def load_model_from_gcs():
    """Load model directly from Google Cloud Storage during inference using SDK"""
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    blob_name = os.getenv("GCS_BLOB_NAME")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Try to load from GCS first
    if all([bucket_name, blob_name]):
        try:
            logging.info(f"Loading model from GCS during inference: {bucket_name}/{blob_name}")
            
            # Set credentials if provided
            if credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Download model content to memory (not to file)
            model_content = blob.download_as_bytes()
            
            # Save temporarily to load into XGBoost
            temp_model_path = os.path.join(BASE_PATH, "data", "temp_model.json")
            with open(temp_model_path, "wb") as f:
                f.write(model_content)
            
            # Load model
            model = xgb.XGBClassifier()
            model.load_model(temp_model_path)
            
            # Clean up temp file
            os.remove(temp_model_path)
            
            logging.info("✅ Model loaded from GCS during inference")
            return model
            
        except Exception as e:
            logging.warning(f"⚠️ Failed to load model from GCS during inference: {e}")
            logging.info("Falling back to local model file")
    
    # Fallback to local model
    logging.info("Loading model from local file")
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    return model

# Load model and metadata (load metadata once, model during inference)
def load_columns_and_labels():
    """Load column names and label classes (metadata only)"""
    logging.info("Loading metadata...")
    
    with open(COLUMNS_PATH, "r") as f:
        columns = json.load(f)

    with open(LABELS_PATH, "r") as f:
        label_classes = json.load(f)

    return columns, label_classes

# Load metadata once at startup
expected_columns, label_classes = load_columns_and_labels()

app = FastAPI()

# Enums for Input Validation
class Island(str, Enum):
    Torgersen = "Torgersen"
    Biscoe = "Biscoe"
    Dream = "Dream"

class Sex(str, Enum):
    Male = "male"
    Female = "female"

# Pydantic Input Schema
class PenguinFeatures(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    year: int
    sex: Sex
    island: Island

# Helper function to preprocess input
def preprocess_features(features: PenguinFeatures, expected_columns: list) -> pd.DataFrame:
    input_dict = features.model_dump()
    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df, columns=["sex", "island"])
    df = df.reindex(columns=expected_columns, fill_value=0)
    df = df.astype(float)
    return df

# Initialize FastAPI App
@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(features: PenguinFeatures):
    logging.info("Received prediction request")

    try:
        # Load model from GCS during inference using SDK
        model = load_model_from_gcs()
        
        X_input = preprocess_features(features, expected_columns)
        pred = model.predict(X_input.values)[0]
        predicted_label = label_classes[int(pred)]
        logging.info(f"Predicted: {predicted_label}")
        return {"prediction": predicted_label}

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed due to internal error.")