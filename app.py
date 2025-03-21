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

# Custom CSS for sleek white theme styling
st.markdown(
    """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        color: #1f2937;
        font-family: 'Plus Jakarta Sans', sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Main container styling */
    .main {
        background-color: #ffffff;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%239C92AC' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E"),
            linear-gradient(135deg, rgba(240, 249, 255, 0.5) 0%, rgba(255, 255, 255, 0.8) 100%);
    }
    
    .block-container {
        padding: 2rem 1rem 10rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Header styling with gradient text */
    .main-title {
        background: linear-gradient(90deg, #0369a1, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -0.02em;
    }
    
    .sub-title {
        color: #64748b;
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* Section header */
    h3, .section-header {
        color: #0f172a;
        font-weight: 600;
        margin-top: 1.5rem;
        font-size: 20px;
    }
    
    /* Input form styling */
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #0ea5e9;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);
    }
    
    .stSelectbox > div > div {
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0ea5e9;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);
    }
    
    /* Card container */
    .card-container {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        margin-bottom: 24px;
    }
    
    /* Metric box styling */
    .metric-box {
        background: white;
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03), 
                    0 4px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 35px rgba(0, 0, 0, 0.04), 
                    0 10px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-label {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-value {
        background: linear-gradient(135deg, #0369a1, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: bold;
        letter-spacing: -0.02em;
    }
    
    .metric-value-alt {
        background: linear-gradient(135deg, #0d9488, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: bold;
        letter-spacing: -0.02em;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #0369a1, #0ea5e9);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.2);
        transition: all 0.3s ease;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0284c7, #38bdf8);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(14, 165, 233, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(14, 165, 233, 0.2);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(90deg, #0d9488, #0ea5e9);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(13, 148, 136, 0.2);
        transition: all 0.3s ease;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #0f766e, #06b6d4);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(13, 148, 136, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 10px;
        color: #0f172a;
        font-weight: 500;
        transition: background 0.2s;
        border: 1px solid #f1f5f9;
        padding: 12px 20px;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9;
    }
    
    .streamlit-expanderContent {
        background: #ffffff;
        border-radius: 0 0 10px 10px;
        padding: 1.5rem;
        border: 1px solid #f1f5f9;
        border-top: none;
    }
    
    /* Warning messages */
    .stAlert {
        background-color: rgba(250, 204, 21, 0.1);
        border: 1px solid rgba(250, 204, 21, 0.2);
        border-radius: 10px;
    }
    
    .stAlert > div > div > div > div {
        color: #854d0e;
    }
    
    /* Error messages */
    .element-container .stAlert[data-baseweb="notification"] {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 10px;
    }
    
    .element-container .stAlert[data-baseweb="notification"] > div > div > div > div {
        color: #b91c1c;
    }
    
    /* DataFrame styling */
    .dataframe {
        background-color: #ffffff;
        color: #1e293b;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }
    
    .dataframe th {
        background-color: #f8fafc;
        color: #0f172a;
        padding: 12px;
        font-weight: 600;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .dataframe td {
        background-color: #ffffff;
        color: #1e293b;
        padding: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    /* Divider styling */
    hr {
        border-color: #e2e8f0;
        margin: 2rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #f1f5f9;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Container divs for better organization */
    .input-container {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        margin-bottom: 24px;
    }
    
    .results-container {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        margin-top: 24px;
        margin-bottom: 24px;
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
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<h3 class="section-header">Enter Your Financial Information</h3>', unsafe_allow_html=True)

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

# Buttons in a row with more space
st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
col_btn1, col_space, col_btn2 = st.columns([1, 0.2, 1])
with col_btn1:
    calculate = st.button("Calculate Tax")
with col_btn2:
    reset = st.button("Reset")

st.markdown('</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-header">Tax Analysis Results</h3>', unsafe_allow_html=True)
            
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
                    f'<div class="metric-value-alt">${predicted_tax:,.2f}</div></div>',
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
            
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

            # Plot comparison with light theme styling
            st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
            st.markdown('<h3 class="section-header">Tax Calculation Comparison</h3>', unsafe_allow_html=True)
            
            # Configure plot with light theme
            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')
            
            # Create gradient color for bars
            bar_colors = ['#0ea5e9', '#0d9488']
            ax.bar(['Traditional', 'ML Prediction'], [traditional_tax, predicted_tax], color=bar_colors)
            
            # Style the plot
            ax.set_ylabel('Tax Amount ($)', fontsize=12, color='#0f172a')
            ax.set_title('Tax Calculation Comparison', fontsize=14, pad=15, color='#0f172a')
            ax.set_ylim(0, max(traditional_tax, predicted_tax) * 1.2)
            ax.tick_params(colors='#1e293b')
            ax.spines['bottom'].set_color('#e2e8f0')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e2e8f0')
            ax.grid(axis='y', linestyle='--', alpha=0.2, color='#94a3b8')
            
            # Add value labels
            for i, v in enumerate([traditional_tax, predicted_tax]):
                ax.text(i, v + max(traditional_tax, predicted_tax) * 0.05, f'${v:,.2f}', 
                        ha='center', fontsize=10, color='#0f172a')
            
            fig.tight_layout()
            st.pyplot(fig)
            
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"ML prediction failed: {e}")
            # Only show traditional tax without redundant "Calculated Tax"
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-header">Tax Analysis Results</h3>', unsafe_allow_html=True)
            st.markdown(
                '<div class="metric-box"><div class="metric-label">Traditional Tax Calculation</div>'
                f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">Tax Analysis Results</h3>', unsafe_allow_html=True)
        st.markdown(
            '<div class="metric-box"><div class="metric-label">Traditional Tax Calculation</div>'
            f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

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
