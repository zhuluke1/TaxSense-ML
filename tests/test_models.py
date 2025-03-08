from joblib import load
import pandas as pd

# Load the trained model
model = load("tax_model_test.joblib")

# Prepare test data (make sure column names match training data)
test_data = pd.DataFrame([[60000, 12000]], columns=["income", "deductions"])

# Make a prediction
predicted_tax = model.predict(test_data)

print(f"Predicted Tax for income=60000, deductions=12000: {predicted_tax[0]:.2f}")
