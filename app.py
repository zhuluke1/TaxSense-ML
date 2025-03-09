import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.ml_models import TaxPredictor
from src.tax_calculator import TaxCalculator
from src.data_processing import DataProcessor

st.set_page_config(page_title="TaxSense ML", page_icon="📊")

st.title("TaxSense ML: Tax Prediction System")
st.write("Predict your tax liability using machine learning")

# Initialize components
predictor = TaxPredictor()
calculator = TaxCalculator()
processor = DataProcessor()

try:
    predictor.load_model('models/tax_model.joblib')
    processor.load_scaler('models/scaler.joblib')
    model_loaded = True
except FileNotFoundError:
    st.warning("No trained model or scaler found. Using traditional calculation method.")
    model_loaded = False

# Input form
st.subheader("Enter Your Financial Information")
col1, col2, col3 = st.columns(3)

with col1:
    income = st.number_input("Annual Income ($)", min_value=0, value=50000)
with col2:
    deductions = st.number_input("Total Deductions ($)", min_value=0, value=12000)
with col3:
    filing_status = st.selectbox(
        "Filing Status",
        options=['single', 'married', 'head_of_household'],
        index=0
    )

if st.button("Calculate Tax"):
    # Traditional calculation
    traditional_tax = calculator.calculate_tax(income, deductions, filing_status)
    
    # ML prediction if model is loaded
    if model_loaded:
        try:
            input_data = pd.DataFrame([[income, deductions]], columns=['income', 'deductions'])
            processed_input = processor.preprocess_features(input_data)  # Add this method
            predicted_tax = predictor.predict_tax(processed_input)[0]
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Traditional Tax Calculation", f"${traditional_tax:,.2f}")
            with col2:
                st.metric("ML-Based Prediction", f"${predicted_tax:,.2f}")
                
            # Plot comparison
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(['Traditional', 'ML Prediction'], [traditional_tax, predicted_tax])
            ax.set_ylabel('Tax Amount ($)')
            ax.set_title('Tax Calculation Comparison')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"ML prediction failed: {e}")
            st.metric("Calculated Tax", f"${traditional_tax:,.2f}")
    else:
        st.metric("Calculated Tax", f"${traditional_tax:,.2f}")

# Sample Data Viewer
with st.expander("View Sample Tax Data"):
    sample_data = calculator.load_sample_data()
    if sample_data is not None:
        st.dataframe(sample_data)
    else:
        st.write("No sample data available.")

# Additional Information
with st.expander("How it works"):
    st.write("""
    This tax prediction system uses two methods:
    1. Traditional tax bracket calculation based on 2024 tax rates
    2. Machine learning prediction based on historical tax data
    
    The ML model is trained on patterns in historical tax data and can capture 
    complex relationships between income, deductions, and tax liability.
    
    The system supports three filing statuses:
    - Single
    - Married Filing Jointly
    - Head of Household
    
    Tax brackets and rates are based on 2024 IRS guidelines.
    """)

# Footer
st.markdown("---")
st.markdown("*Note: This is an estimation tool and should not be used as official tax advice.*")
