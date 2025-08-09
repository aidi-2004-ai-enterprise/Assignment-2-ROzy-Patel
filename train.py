import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import xgboost as xgb
import os
import json

# Load dataset
df = sns.load_dataset("penguins")
df = df.dropna()

# Label encode target
label_encoder = LabelEncoder()
df["species"] = label_encoder.fit_transform(df["species"])

# One-hot encode categorical variables
df = pd.get_dummies(df, columns=["sex", "island"])

# Split into features and target
X = df.drop("species", axis=1)
y = df["species"]

# Save column structure for inference
os.makedirs("app/data", exist_ok=True)
with open("app/data/columns.json", "w") as f:
    json.dump(list(X.columns), f)

# Save label classes
with open("app/data/label_classes.json", "w") as f:
    json.dump(list(label_encoder.classes_), f)

# Train-test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train XGBoost model
model = xgb.XGBClassifier(
    max_depth=3,
    n_estimators=100,
    use_label_encoder=False,
    eval_metric="mlogloss",
    verbosity=0
)

model.fit(X_train, y_train)

# Evaluate
print("Training complete.")
print("Train F1 Score:", f1_score(y_train, model.predict(X_train), average="macro"))
print("Test F1 Score:", f1_score(y_test, model.predict(X_test), average="macro"))
print("\nClassification Report (Test):\n")
print(classification_report(y_test, model.predict(X_test), target_names=label_encoder.classes_))

# Save trained model
model.save_model("app/data/model.json")
print("Model saved to app/data/model.json")
