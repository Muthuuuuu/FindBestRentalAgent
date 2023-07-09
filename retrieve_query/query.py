import pandas as pd

def find_highest_transaction_agent(dataset_path, district):
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(dataset_path)
    
    # Filter transactions by the specified district
    district_transactions = df[df['district'] == district]
    
    # Count the number of transactions for each agent
    agent_transactions = district_transactions['agent'].value_counts()
    
    # Find the agent with the highest number of transactions
    highest_transaction_agent = agent_transactions.idxmax()
    
    return highest_transaction_agent

# Usage example
dataset_path = 'property_transactions.csv'  # Replace with the actual path to your dataset file
district = 'District X'  # Replace with the desired district
highest_transaction_agent = find_highest_transaction_agent(dataset_path, district)
print(f"The property agent with the highest number of transactions in {district} is: {highest_transaction_agent}")
