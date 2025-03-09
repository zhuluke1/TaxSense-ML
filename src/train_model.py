import os
from ml_models import TaxPredictor
from tax_calculator import TaxCalculator
from data_processing import DataProcessor

def train_initial_model(samples=10000):
    """Generate synthetic data and train the initial model."""
    print("Generating synthetic training data...")
    calculator = TaxCalculator()
    data = calculator.generate_training_data(num_samples=samples)
    print(data.describe())  # Check ranges of income, deductions, tax_liability
    
    print("Processing data...")
    processor = DataProcessor()
    # Fit the scaler on the training data
    features = data[['income', 'deductions']]
    processor.scaler.fit(features)  # Fit the scaler here
    X = processor.preprocess_features(data)  # Now transform
    
    print("Training model...")
    predictor = TaxPredictor()
    predictor.train(X, data['tax_liability'])
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save model and scaler
    print("Saving model and scaler...")
    predictor.save_model('models/tax_model.joblib')
    processor.save_scaler('models/scaler.joblib')
    
    print("Training complete! You can now use the model for predictions.")

if __name__ == "__main__":
    train_initial_model()
