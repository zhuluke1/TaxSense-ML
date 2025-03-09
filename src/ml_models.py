from sklearn.linear_model import Lasso
from joblib import dump, load
import pandas as pd
import numpy as np

class TaxPredictor:
    def __init__(self):
        """Initialize the tax prediction model with Lasso (L1)."""
        self.model = Lasso(alpha=1.0)  # alpha controls regularization strength

    def train(self, X, y):
        """Train the model with features (X) and target (y)."""
        self.model.fit(X, y)

    def predict_tax(self, features):
        """Predict tax liability for given features."""
        return self.model.predict(features)

    def save_model(self, filepath):
        """Save the trained model to a file."""
        dump(self.model, filepath)

    def load_model(self, filepath):
        """Load a trained model from a file."""
        self.model = load(filepath)
        