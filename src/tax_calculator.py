import pandas as pd
import numpy as np

class TaxCalculator:
    def __init__(self, tax_tables_file='data/tax_tables_2024.csv'):
        """Initialize with tax brackets from file."""
        try:
            self.tax_tables = pd.read_csv(tax_tables_file)
            required_cols = ['filing_status', 'bracket_start', 'bracket_end', 'tax_rate']
            if not all(col in self.tax_tables.columns for col in required_cols):
                raise ValueError("Tax tables missing required columns")
        except FileNotFoundError:
            print(f"Error: {tax_tables_file} not found.")
            self.tax_tables = None
        except Exception as e:
            print(f"Error loading tax tables: {e}")
            self.tax_tables = None
        
    def calculate_tax(self, income, deductions, filing_status='single'):
        """Calculate tax using traditional tax bracket method."""
        if self.tax_tables is None:
            return 0  # Or raise an error
        taxable_income = max(0, income - deductions)
        total_tax = 0
        
        # Get brackets for filing status
        status_brackets = self.tax_tables[self.tax_tables['filing_status'] == filing_status].sort_values('bracket_start')
        if status_brackets.empty:
            print(f"Warning: No brackets for {filing_status}")
            return 0
        
        for _, bracket in status_brackets.iterrows():
            if taxable_income > bracket['bracket_start']:
                taxable_in_bracket = min(
                    taxable_income - bracket['bracket_start'],
                    bracket['bracket_end'] - bracket['bracket_start']
                )
                total_tax += taxable_in_bracket * bracket['tax_rate']
            else:
                break
                
        return total_tax

    def generate_training_data(self, num_samples=1000):
        """Generate synthetic data for model training."""
        if self.tax_tables is None:
            print("Error: No tax tables available")
            return None
        incomes = np.random.uniform(20000, 150000, num_samples)  # Lower max to 150k
        deduction_rates = np.random.uniform(0.05, 0.30, num_samples)
        deductions = incomes * deduction_rates
        statuses = np.random.choice(['single', 'married', 'head_of_household'], num_samples)
        
        taxes = [self.calculate_tax(inc, ded, status) 
                for inc, ded, status in zip(incomes, deductions, statuses)]
        
        return pd.DataFrame({
            'income': incomes,
            'deductions': deductions,
            'filing_status': statuses,
            'tax_liability': taxes
    })

    def load_sample_data(self, filepath='data/sample_finances.csv'):
        """Load and return sample financial data."""
        try:
            return pd.read_csv(filepath)
        except FileNotFoundError:
            print(f"Error: {filepath} not found.")
            return None