import pandas as pd
import time
import os

def process_emails():
    # Read the CSV file
    df = pd.read_csv('dummy_data.csv')
    
    # Create or load processed entries file
    processed_file = 'processed_entries.csv'
    if not os.path.exists(processed_file):
        pd.DataFrame(columns=['email', 'company', 'processed']).to_csv(processed_file, index=False)
    
    processed_df = pd.read_csv(processed_file)
    
    # Process each unprocessed entry
    for index, row in df[df['processed'] == 0].iterrows():
        print(f"Processing: {row['email']} from {row['company']}")
        
        # Add to processed entries
        processed_df = pd.concat([processed_df, pd.DataFrame([row])], ignore_index=True)
        processed_df.to_csv(processed_file, index=False)
        
        # Update processed flag in original file
        df.at[index, 'processed'] = 1
        df.to_csv('dummy_data.csv', index=False)
        
        # Wait for 5 seconds
        time.sleep(5)
    
    print("All entries processed!")

if __name__ == "__main__":
    process_emails() 