import pandas as pd
import time
import os
from email_template import generate_email_content

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
        print(f"\nProcessing application for: {row['company']}")
        
        # Generate email content
        email_content = generate_email_content(row['company'])
        
        # Print email details
        print("\nEmail Subject:", email_content['subject'])
        print("\nEmail Body:")
        print("=" * 50)
        print(email_content['body'])
        print("=" * 50)
        
        # Add to processed entries
        processed_df = pd.concat([processed_df, pd.DataFrame([row])], ignore_index=True)
        processed_df.to_csv(processed_file, index=False)
        
        # Update processed flag in original file
        df.at[index, 'processed'] = 1
        df.to_csv('dummy_data.csv', index=False)
        
        # Wait for 5 seconds before next entry
        print("\nWaiting 5 seconds before next application...\n")
        time.sleep(5)
    
    print("All entries processed!")

if __name__ == "__main__":
    process_emails() 