from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

class TaxPredictor:
    def __init__(self):
        """Initialize the tax prediction model."""
        self.model = LinearRegression()

    def train(self, X, y):
        """Train the model with features (X) and target (y)."""
        self.model.fit(X, y)

    def predict_tax(self, features):
        """Predict tax liability for given features."""
        return self.model.predict(features)

    def save_model(self, filepath):
        """Save the trained model to a file."""
        from joblib import dump
        dump(self.model, filepath)

    def load_model(self, filepath):
        """Load a trained model from a file."""
        from joblib import load
        self.model = load(filepath)

# Test the class if run directly
if __name__ == "__main__":
    # Dummy data: income, deductions as features; tax as target
    X = pd.DataFrame({
        'income': [50000, 75000, 100000],
        'deductions': [10000, 15000, 20000]
    })
    y = np.array([8000, 12000, 18000])  # Dummy tax values

    # Create and train the model
    predictor = TaxPredictor()
    predictor.train(X, y)

    # Test prediction
    sample = X.iloc[0].values.reshape(1, -1)  # First row: [50000, 10000]
    pred = predictor.predict_tax(sample)
    print(f"Predicted tax for income=50000, deductions=10000: {pred[0]:.2f}")

    # Save the model (optional)
    predictor.save_model('tax_model_test.joblib')
    print("Model saved to tax_model_test.joblib")
        