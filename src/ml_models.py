from sklearn.linear_model import LinearRegression
import pandas as pd

class TaxPredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_tax(self, features):
        return self.model.predict(features)