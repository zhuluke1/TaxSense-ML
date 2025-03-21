import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from src.ml_models import TaxPredictor
from src.tax_calculator import TaxCalculator
from src.data_processing import DataProcessor
from io import BytesIO  # Add for Excel export

# Set page config with a custom icon
st.set_page_config(page_title="TaxGenius ML", page_icon="💰", layout="wide")

# Custom CSS for sleek, modern styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Main container styling */
    .main > div {
        padding: 1rem 2rem 4rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .main-title {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(90deg, #0066FF, #2684FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: rgba(49, 51, 63, 0.7);
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(209, 213, 219, 0.3);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(39, 40, 44, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px -3px rgba(39, 40, 44, 0.07);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(209, 213, 219, 0.4);
    }
    
    /* Metric box styling */
    .metric-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-box {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 1.25rem;
        flex: 1;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(209, 213, 219, 0.5);
        transition: all 0.2s ease;
    }
    
    .metric-box:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    
    .metric-box.traditional {
        border-left: 4px solid #3B82F6;
    }
    
    .metric-box.ml {
        border-left: 4px solid #10B981;
    }
    
    /* Form styling */
    .stNumberInput > div > div > input {
        height: 3rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 0 1rem;
        font-size: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    
    .stSelectbox > div > div {
        height: 3rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stSelectbox > div > div:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    
    /* Button styling */
    .stButton > button {
        height: 2.75rem;
        padding: 0 1.5rem;
        background: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: #2563EB;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    .stDownloadButton > button {
        background: #10B981;
        border-radius: 8px;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: #059669;
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
    }
    
    /* Chart styling */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1E293B;
        background: rgba(243, 244, 246, 0.7);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        transition: background 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(243, 244, 246, 1);
    }
    
    .streamlit-expanderContent {
        padding: 1.25rem 0.5rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 4rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(209, 213, 219, 0.3);
    }
    
    /* Progress animation */
    @keyframes shimmer {
        0% {
            background-position: -468px 0;
        }
        100% {
            background-position: 468px 0;
        }
    }
    
    .loading-animation {
        background: linear-gradient(to right, #f6f7f8 8%, #edeef1 18%, #f6f7f8 33%);
        background-size: 800px 104px;
        animation: shimmer 1.5s infinite linear;
        border-radius: 8px;
        height: 60px;
    }
    
    /* Accent color for highlights */
    .accent-text {
        color: #3B82F6;
        font-weight: 500;
    }
    
    /* DataTable styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background-color: #F8FAFC;
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        color: #1E293B;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .dataframe tr:hover {
        background-color: #F8FAFC;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .sub-title {
            font-size: 1rem;
        }
        
        .metric-container {
            flex-direction: column;
            gap: 1rem;
        }
        
        .metric-box {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with updated styling
st.markdown('<div class="main-title">TaxGenius ML</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced tax liability prediction using machine learning</div>', unsafe_allow_html=True)

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

# Input form in a glass card container
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📊 Enter Your Financial Information</div>', unsafe_allow_html=True)

# Use columns for the form layout
col1, col2, col3 = st.columns(3)

with col1:
    income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=1000, format="%d")
with col2:
    deductions = st.number_input("Total Deductions ($)", min_value=0, value=12000, step=1000, format="%d")
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

st.markdown('</div>', unsafe_allow_html=True)  # Close the glass card

# Reset form if clicked
if reset:
    st.session_state.income = 50000
    st.session_state.deductions = 12000
    st.session_state.filing_status = 'single'
    st.rerun()

if calculate:
    # Traditional calculation
    traditional_tax = calculator.calculate_tax(income, deductions, filing_status)
    
    # Results container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💡 Tax Analysis Results</div>', unsafe_allow_html=True)
    
    # ML prediction if model is loaded
    if model_loaded:
        try:
            input_data = pd.DataFrame([[income, deductions]], columns=['income', 'deductions'])
            processed_input = processor.preprocess_features(input_data).values
            predicted_tax = predictor.predict_tax(processed_input)[0]
            
            # Display results in a styled container
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-box traditional"><div class="metric-label">Traditional Calculation</div>'
                f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-box ml"><div class="metric-label">ML-Based Prediction</div>'
                f'<div class="metric-value">${predicted_tax:,.2f}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
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
                label="💾 Export to Excel",
                data=excel_data,
                file_name="tax_calculation_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download-excel"
            )

            # Plot comparison with improved styling
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Tax Calculation Comparison", unsafe_allow_html=True)
            
            # Create a more modern figure
            fig, ax = plt.subplots(figsize=(10, 4.5))
            
            # Use a more professional color palette
            bar_colors = ['#3B82F6', '#10B981']
            
            # Create bar chart
            bars = ax.bar(['Traditional Calculation', 'ML Prediction'], 
                  [traditional_tax, predicted_tax], 
                  color=bar_colors, 
                  width=0.5)
            
            # Add value labels on top of bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                value = traditional_tax if i == 0 else predicted_tax
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01 * max(traditional_tax, predicted_tax),
                       f'${value:,.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            # Customize the figure appearance
            ax.set_ylabel('Tax Amount ($)', fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#DDE1E4')
            ax.spines['bottom'].set_color('#DDE1E4')
            ax.tick_params(axis='both', colors='#64748B')
            ax.set_ylim(0, max(traditional_tax, predicted_tax) * 1.15)
            ax.grid(axis='y', linestyle='-', alpha=0.2)
            
            # Remove the title since we already have one in markdown
            fig.tight_layout()
            
            # Display the plot
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"ML prediction failed: {e}")
            # Only show traditional tax without redundant "Calculated Tax"
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-box traditional"><div class="metric-label">Traditional Calculation</div>'
                f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="metric-box traditional"><div class="metric-label">Traditional Calculation</div>'
            f'<div class="metric-value">${traditional_tax:,.2f}</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close the glass card

# Sample Data Viewer with improved styling
with st.expander("📋 View Sample Tax Data"):
    sample_data = calculator.load_sample_data()
    if sample_data is not None:
        st.dataframe(sample_data.style.format({
            'income': '${:,.2f}',
            'deductions': '${:,.2f}',
            'tax_liability': '${:,.2f}'
        }))
    else:
        st.write("No sample data available.")

# How It Works section with enhanced styling
with st.expander("🧠 How It Works"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Traditional Calculation
        
        This method uses the <span class="accent-text">2024 IRS tax rates</span> and applies standard tax brackets based on your filing status:
        
        1. Calculate taxable income (income minus deductions)
        2. Apply progressive tax rates to different portions of income
        3. Sum up tax amounts from each bracket
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### ML-Based Prediction
        
        The <span class="accent-text">machine learning model</span> is trained on historical tax data to identify patterns:
        
        1. Preprocesses financial data using feature scaling
        2. Uses a Lasso regression algorithm to detect complex relationships
        3. Considers factors that traditional methods might miss
        4. Provides predictions that adapt to changing patterns
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Supported Filing Statuses:
    
    - **Single**: For individuals filing alone
    - **Married Filing Jointly**: For married couples filing together
    - **Head of Household**: For unmarried individuals who pay for keeping up a home
    
    <div style="background-color: #EFF6FF; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #3B82F6;">
    <strong>Note</strong>: Tax brackets and rates are based on 2024 IRS guidelines. Always consult a tax professional for official advice.
    </div>
    """, unsafe_allow_html=True)

# Footer with sleek styling
st.markdown(
    '<div class="footer">© 2025 TaxGenius ML • This application is for educational purposes only • Not financial advice</div>',
    unsafe_allow_html=True
)
