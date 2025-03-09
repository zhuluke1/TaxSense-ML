import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from joblib import dump, load

class DataProcessor:
    def __init__(self):
        """Initialize the data processor with a scaler."""
        self.scaler = StandardScaler()
    
    def load_data(self, filepath):
        """Load data from CSV file."""
        return pd.read_csv(filepath)
    
    def preprocess_features(self, df):
        """Preprocess features for model training/prediction."""
        # Ensure required columns exist
        required_cols = ['income', 'deductions']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Data must contain columns: {required_cols}")
        
        # Handle missing values
        df = df.fillna({
            'income': df['income'].mean(),
            'deductions': df['deductions'].median()
        })
        
        # Debug: Show raw and scaled values
        print("Raw input values:", df[required_cols].values)
        features = df[required_cols]
        scaled_features = self.scaler.transform(features)  # Use loaded scaler
        print("Scaled input values:", scaled_features)
        return pd.DataFrame(scaled_features, columns=required_cols)
    
    def prepare_training_data(self, filepath, test_size=0.2, random_state=42):
        """Load, preprocess, and split data for training."""
        df = self.load_data(filepath)
        X = self.preprocess_features(df)
        y = df['tax_liability']
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def save_scaler(self, filepath):
        """Save the fitted scaler for later use."""
        dump(self.scaler, filepath)
    
    def load_scaler(self, filepath):
        """Load a previously fitted scaler."""
        from joblib import load
        self.scaler = load(filepath)
        print("Scaler loaded with mean:", self.scaler.mean_, "scale:", self.scaler.scale_)  # Debug
