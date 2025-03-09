import os
from ml_models import TaxPredictor
from tax_calculator import TaxCalculator
from data_processing import DataProcessor

def train_initial_model(samples=10000):
    """Generate synthetic data and train the initial model."""
    print("Generating synthetic training data...")
    calculator = TaxCalculator()
    data = calculator.generate_training_data(num_samples=samples)
    
    print("Processing data...")
    processor = DataProcessor()
    X = processor.preprocess_features(data)
    y = data['tax_liability']
    
    print("Training model...")
    predictor = TaxPredictor()
    predictor.train(X, y)
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save model and scaler
    print("Saving model and scaler...")
    predictor.save_model('models/tax_model.joblib')
    processor.save_scaler('models/scaler.joblib')
    
    print("Training complete! You can now use the model for predictions.")

if __name__ == "__main__":
    train_initial_model()