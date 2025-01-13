from email_sender import EmailSender
import time

def test_email_send():
    print("Testing email sending functionality...")
    
    # Initialize email sender
    try:
        email_sender = EmailSender()
    except ValueError as e:
        print(f"Error: {str(e)}")
        return
    
    # Test email content
    subject = "Test Email - Please Ignore"
    body = """This is a test email to verify the email sending functionality.
    
If you receive this, the email system is working correctly.

Best regards,
Yash"""
    
    recipient = "yash.sh0031@gmail.com"
    
    print(f"\nSending test email to: {recipient}")
    print("\nEmail content:")
    print("-" * 40)
    print(f"Subject: {subject}")
    print(f"\nBody:\n{body}")
    print("-" * 40)
    
    # Send the email
    success = email_sender.send_email(
        subject=subject,
        body=body,
        recipient_email=recipient
    )
    
    if success:
        print("\nTest email sent successfully!")
    else:
        print("\nFailed to send test email. Please check the error messages above.")

if __name__ == "__main__":
    test_email_send() 