import pandas as pd
import numpy as np
import os

# Define the possible responses
responses = ['Yes', 'No', 'Not used', 'Consider to use', 'Testing', 'Implementing', 'Operational', 'Partially']

# Weights for before (lower maturity: more No, Not used, Consider)
weights_before = [0.1, 0.3, 0.2, 0.15, 0.1, 0.05, 0.05, 0.05]

# Weights for after (higher maturity: more Yes, Operational, etc.)
weights_after = [0.25, 0.1, 0.05, 0.1, 0.1, 0.15, 0.2, 0.05]

# Number of companies
num_companies = 1000

# Map Q1-Q11 to descriptive names
question_map = {
    'Q1': 'Digital Strategy Defined',
    'Q2': 'Digital Strategy Implemented',
    'Q3': 'Employees Trained in Digital Skills',
    'Q4': 'Remote Work Infrastructure',
    'Q5': 'Digital Tools Adoption',
    'Q6': 'User Experience Priority',
    'Q7': 'Employee Well-being Monitoring',
    'Q8': 'Data Security Measures',
    'Q9': 'Data Usage for Decision Making',
    'Q10': 'AI and Automation Usage',
    'Q11': 'Sustainability in Digitalization'
}

questions = list(question_map.values())

# Generate data
data_before = []
data_after = []

try:
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    for company_id in range(1, num_companies + 1):
        company_data_before = {'Company_ID': company_id}
        company_data_after = {'Company_ID': company_id}
        
        for q_text in questions: 
            company_data_before[q_text] = np.random.choice(responses, p=weights_before)
            company_data_after[q_text] = np.random.choice(responses, p=weights_after)
            
        data_before.append(company_data_before)
        data_after.append(company_data_after)

    # Create DataFrames
    df_before = pd.DataFrame(data_before)
    df_after = pd.DataFrame(data_after)

    # Save to Excel in data/ folder
    df_before.to_excel('data/rawdma_before.xlsx', index=False)
    df_after.to_excel('data/rawdma_after.xlsx', index=False)

    print("Synthetic data generated and saved to data/rawdma_before.xlsx and data/rawdma_after.xlsx.")

except Exception as e:
    print(f"Error generating data: {e}")
