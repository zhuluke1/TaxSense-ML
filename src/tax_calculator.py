import pandas as pd
import numpy as np

class TaxCalculator:
    def __init__(self, tax_tables_file='data/tax_tables_2024.csv'):
        """Initialize with tax brackets from file."""
        self.tax_tables = pd.read_csv(tax_tables_file)
        
    def calculate_tax(self, income, deductions, filing_status='single'):
        """Calculate tax using traditional tax bracket method."""
        taxable_income = max(0, income - deductions)
        total_tax = 0
        
        # Get brackets for filing status
        status_brackets = self.tax_tables[self.tax_tables['filing_status'] == filing_status].sort_values('bracket_start')
        
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
        # Generate random incomes between 20k and 500k
        incomes = np.random.uniform(20000, 500000, num_samples)
        
        # Generate reasonable deductions (between 5% and 30% of income)
        deduction_rates = np.random.uniform(0.05, 0.30, num_samples)
        deductions = incomes * deduction_rates
        
        # Generate random filing statuses
        statuses = np.random.choice(['single', 'married', 'head_of_household'], num_samples)
        
        # Calculate actual tax for each case
        taxes = [self.calculate_tax(inc, ded, status) 
                for inc, ded, status in zip(incomes, deductions, statuses)]
        
        # Create DataFrame
        return pd.DataFrame({
            'income': incomes,
            'deductions': deductions,
            'filing_status': statuses,
            'tax_liability': taxes
        })

    def load_sample_data(self, filepath='data/sample_finances.csv'):
        """Load and return sample financial data."""
        return pd.read_csv(filepath)
