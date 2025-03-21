from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import joblib

# Load trained model
model = joblib.load("models/compression_model.pkl")

# Define input type (2 features: file size & entropy)
initial_type = [("float_input", FloatTensorType([None, 2]))]

# Convert to ONNX format
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Save ONNX model
with open("models/compression_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("Model successfully converted to ONNX format!")
