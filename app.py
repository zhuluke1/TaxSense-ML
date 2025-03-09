import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from src.ml_models import TaxPredictor
from src.tax_calculator import TaxCalculator
from src.data_processing import DataProcessor
from io import BytesIO  # Add for Excel export

# Set page config with a custom icon
st.set_page_config(page_title="TaxSense ML", page_icon="💰", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1F2A44;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 18px;
        color: #4A5568;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-box {
        background-color: #F7FAFC;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        font-size: 16px;
        color: #718096;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #2D3748;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #A0AEC0;
        margin-top: 50px;
    }
    .stButton>button {
        background-color: #2B6CB0;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle with custom styling
st.markdown('<div class="main-title">TaxSense ML: Tax Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predict your tax liability using machine learning</div>', unsafe_allow_html=True)

# Initialize components
predictor = TaxPredictor()
calculator = TaxCalculator()
processor = DataProcessor()

# Load model and scaler
try:
    predictor.load_model('models/tax_model.joblib')
    processor.load_scaler('models/scaler.joblib')
    model_loaded = True
except FileNotFoundError:
    st.warning("No trained model or scaler found. Using traditional calculation method.")
    model_loaded = False

# Input form in a container
with st.container():
    st.subheader("Enter Your Financial Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=1000)
    with col2:
        deductions = st.number_input("Total Deductions ($)", min_value=0, value=12000, step=1000)
    with col3:
        filing_status = st.selectbox(
            "Filing Status",
            options=['single', 'married', 'head_of_household'],
            index=0
        )

    # Input validation
    if deductions > income:
        st.error("Deductions cannot exceed income. Please adjust your inputs.")
        st.stop()

    # Buttons in a row
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        calculate = st.button("Calculate Tax")
    with col_btn2:
        reset = st.button("Reset")

# Reset form if clicked
if reset:
    st.session_state.income = 50000
    st.session_state.deductions = 12000
    st.session_state.filing_status = 'single'
    st.rerun()

if calculate:
    # Traditional calculation
    traditional_tax = calculator.calculate_tax(income, deductions, filing_status)
    
    # ML prediction if model is loaded
    if model_loaded:
        try:
            input_data = pd.DataFrame([[income, deductions]], columns=['income', 'deductions'])
            processed_input = processor.preprocess_features(input_data).values
            predicted_tax = predictor.predict_tax(processed_input)[0]
            
            # Display results in a styled container
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        '<div class="metric-box"><div class="metric-label">Traditional Tax Calculation</div>'
                        f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        '<div class="metric-box"><div class="metric-label">ML-Based Prediction</div>'
                        f'<div class="metric-value">${predicted_tax:,.2f}</div></div>',
                        unsafe_allow_html=True
                    )

                # Export to Excel
                result_df = pd.DataFrame({
                    'Method': ['Traditional Tax Calculation', 'ML-Based Prediction'],
                    'Tax Amount ($)': [traditional_tax, predicted_tax]
                })
                # Use BytesIO to create an in-memory Excel file
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name='Tax Results')
                excel_data = output.getvalue()

                st.download_button(
                    label="Export to Excel",
                    data=excel_data,
                    file_name="tax_calculation_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download-excel"
                )

                # Plot comparison
                st.markdown("### Tax Calculation Comparison")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(['Traditional', 'ML Prediction'], [traditional_tax, predicted_tax], color=['#2B6CB0', '#68D391'])
                ax.set_ylabel('Tax Amount ($)', fontsize=12)
                ax.set_title('Tax Calculation Comparison', fontsize=14, pad=15)
                ax.set_ylim(0, max(traditional_tax, predicted_tax) * 1.2)
                for i, v in enumerate([traditional_tax, predicted_tax]):
                    ax.text(i, v + max(traditional_tax, predicted_tax) * 0.05, f'${v:,.2f}', ha='center', fontsize=10)
                st.pyplot(fig)
        except Exception as e:
            st.error(f"ML prediction failed: {e}")
            # Only show traditional tax without redundant "Calculated Tax"
            with st.container():
                st.markdown(
                    '<div class="metric-box"><div class="metric-label">Traditional Tax Calculation</div>'
                    f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                    unsafe_allow_html=True
                )
    else:
        with st.container():
            st.markdown(
                '<div class="metric-box"><div class="metric-label">Traditional Tax Calculation</div>'
                f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                unsafe_allow_html=True
            )

# Sample Data Viewer
with st.expander("View Sample Tax Data"):
    sample_data = calculator.load_sample_data()
    if sample_data is not None:
        st.dataframe(sample_data.style.format({
            'income': '${:,.2f}',
            'deductions': '${:,.2f}',
            'tax_liability': '${:,.2f}'
        }))
    else:
        st.write("No sample data available.")

# Additional Information
with st.expander("How It Works"):
    st.write("""
    **TaxSense ML** uses two methods to estimate your tax liability:
    - **Traditional Tax Bracket Calculation**: Based on 2024 IRS tax rates, this method applies standard tax brackets for your filing status.
    - **Machine Learning Prediction**: A Lasso regression model trained on historical tax data predicts your tax liability by analyzing patterns in income and deductions.

    ### Supported Filing Statuses:
    - **Single**
    - **Married Filing Jointly**
    - **Head of Household**

    ### How the ML Model Works:
    The ML model is trained on synthetic data simulating various income levels, deductions, and filing statuses. It uses a Lasso regression algorithm to identify relationships between inputs and tax outcomes, providing a prediction that can adapt to complex patterns.

    **Note**: Tax brackets and rates are based on 2024 IRS guidelines. Always consult a tax professional for official advice.
    """)

# Footer
st.markdown('<div class="footer">© 2025 TaxSense ML. This is an estimation tool and should not be used as official tax advice.</div>', unsafe_allow_html=True)