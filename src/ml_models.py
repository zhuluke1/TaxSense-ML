from sklearn.linear_model import LinearRegression
import pandas as pd

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