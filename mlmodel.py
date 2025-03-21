# mlmodel.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Ensure the 'models' directory exists
if not os.path.exists('models'):
    os.makedirs('models')

# Sample dataset (File Size, Entropy, Best Compression Method)
data = {
    "file_size_kb": [10, 50, 200, 500, 1000, 5000],
    "entropy": [0.1, 0.4, 0.8, 0.9, 0.6, 0.3],
    "best_method": [0, 1, 2, 1, 0, 2]  # 0=Brotli, 1=Bzip2, 2=Huffman
}

df = pd.DataFrame(data)

# Features (X) and Labels (y)
X = df[["file_size_kb", "entropy"]]
y = df["best_method"]

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Save the trained model as a .pkl file
joblib.dump(model, "models/compression_model.pkl")

print("Model trained and saved successfully!")