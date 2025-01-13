import pandas as pd
import time
import os
from email_template import generate_email_content
from email_sender import EmailSender
from dotenv import load_dotenv

def process_emails():
    # Load environment variables
    load_dotenv()
    
    # Initialize email sender
    try:
        email_sender = EmailSender()
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please update the .env file with your email credentials")
        return
    
    # Read the CSV file
    df = pd.read_csv('dummy_data.csv')
    
    # Create or load processed entries file
    processed_file = 'processed_entries.csv'
    if not os.path.exists(processed_file):
        pd.DataFrame(columns=['email', 'company', 'processed']).to_csv(processed_file, index=False)
    
    processed_df = pd.read_csv(processed_file)
    
    # Get resume path
    resume_path = 'Yash-Sharma-Resume.pdf'
    if not os.path.exists(resume_path):
        print(f"Warning: Resume file not found at {resume_path}")
        resume_path = None
    
    # Process each unprocessed entry
    for index, row in df[df['processed'] == 0].iterrows():
        company_name = row['company']
        recipient_email = row['email']
        
        print(f"\nProcessing application for: {company_name}")
        print(f"Sending to: {recipient_email}")
        
        # Generate email content with Anthropic enhancement
        email_content = generate_email_content(company_name)
        
        # Print email details
        print("\nEmail Subject:", email_content['subject'])
        print("\nEmail Body:")
        print("=" * 50)
        print(email_content['body'])
        print("=" * 50)
        
        # Send email
        print(f"\nSending email to {company_name} ({recipient_email})...")
        success = email_sender.send_email(
            subject=email_content['subject'],
            body=email_content['body'],
            recipient_email=recipient_email,
            resume_path=resume_path
        )
        
        if success:
            # Add to processed entries
            processed_df = pd.concat([processed_df, pd.DataFrame([row])], ignore_index=True)
            processed_df.to_csv(processed_file, index=False)
            
            # Update processed flag in original file
            df.at[index, 'processed'] = 1
            df.to_csv('dummy_data.csv', index=False)
            
            print(f"Successfully sent email to {company_name} ({recipient_email})")
        else:
            print(f"Failed to send email to {company_name} ({recipient_email}), will retry in next run")
        
        # Wait between emails to avoid rate limiting
        print("\nWaiting 10 seconds before next application...\n")
        time.sleep(10)
    
    print("All entries processed!")

if __name__ == "__main__":
    process_emails() 