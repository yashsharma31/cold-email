from email_sender import EmailSender
from email_template import generate_email_content

def test_email():
    # Initialize email sender
    try:
        email_sender = EmailSender()
    except ValueError as e:
        print(f"Error: {str(e)}")
        return
    
    # Test company details
    test_company = "Test Company"
    test_recipient = "yash.sh0031@gmail.com"  # Sending to yourself for testing
    
    # Generate test email content
    email_content = generate_email_content(test_company)
    
    print(f"\nSending test email to: {test_recipient}")
    print("\nEmail Subject:", email_content['subject'])
    print("\nEmail Body:")
    print("=" * 50)
    print(email_content['body'])
    print("=" * 50)
    
    # Try to send the email
    success = email_sender.send_email(
        subject=email_content['subject'],
        body=email_content['body'],
        recipient_email=test_recipient,
        resume_path='Yash-Sharma-Resume.pdf'  # Will show warning if file doesn't exist
    )
    
    if success:
        print("\nTest email sent successfully!")
    else:
        print("\nFailed to send test email. Please check your credentials and try again.")

if __name__ == "__main__":
    test_email() 