class TaxCalculator:
    def __init__(self):
        """Initialize with 2024 tax brackets (single filer)."""
        self.tax_brackets = [
            (0, 11600, 0.10),
            (11600, 47150, 0.12),
            (47150, 100525, 0.22),
            (100525, 191950, 0.24),
            (191950, 243725, 0.32),
            (243725, 609350, 0.35),
            (609350, float('inf'), 0.37)
        ]

    def calculate_tax(self, income, deductions):
        """Calculate tax using traditional tax bracket method."""
        taxable_income = max(0, income - deductions)
        total_tax = 0
        
        for start, end, rate in self.tax_brackets:
            if taxable_income > start:
                taxable_in_bracket = min(taxable_income - start, end - start)
                total_tax += taxable_in_bracket * rate
            else:
                break
                
        return total_tax

    def generate_training_data(self, num_samples=1000):
        """Generate synthetic data for model training."""
        import numpy as np
        import pandas as pd
        
        # Generate random incomes between 20k and 500k
        incomes = np.random.uniform(20000, 500000, num_samples)
        
        # Generate reasonable deductions (between 5% and 30% of income)
        deduction_rates = np.random.uniform(0.05, 0.30, num_samples)
        deductions = incomes * deduction_rates
        
        # Calculate actual tax for each case
        taxes = [self.calculate_tax(inc, ded) 
                for inc, ded in zip(incomes, deductions)]
        
        # Create DataFrame
        return pd.DataFrame({
            'income': incomes,
            'deductions': deductions,
            'tax_liability': taxes
        })
