from email_template import generate_email_content
from email_sender import EmailSender
import os

def test_company_email(company_name="Microsoft"):
    print(f"Testing email generation and sending for {company_name}")
    
    # Initialize email sender
    try:
        email_sender = EmailSender()
    except ValueError as e:
        print(f"Error: {str(e)}")
        return
    
    # Generate email content
    email_content = generate_email_content(company_name)
    
    # Print email details
    print("\nGenerated Email Content:")
    print("=" * 50)
    print("Subject:", email_content['subject'])
    print("\nBody:")
    print(email_content['body'])
    print("=" * 50)
    
    # Confirm before sending
    confirm = input("\nWould you like to send this email? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Email sending cancelled.")
        return
    
    # Get resume path
    resume_path = 'Yash-Sharma-Resume.pdf'
    if not os.path.exists(resume_path):
        print(f"Warning: Resume file not found at {resume_path}")
        resume_path = None
    
    # Send to your own email for testing
    recipient_email = "yash.sh0031@gmail.com"
    
    print(f"\nSending email to: {recipient_email}")
    success = email_sender.send_email(
        subject=email_content['subject'],
        body=email_content['body'],
        recipient_email=recipient_email,
        resume_path=resume_path
    )
    
    if success:
        print("\nEmail sent successfully!")
    else:
        print("\nFailed to send email. Please check the error messages above.")

if __name__ == "__main__":
    test_company_email() 