import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import time

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.sender_name = os.getenv('SENDER_NAME')
        
        if not all([self.email_address, self.email_password, self.sender_name]):
            raise ValueError("Please set all required environment variables in .env file")
    
    def setup_smtp(self):
        """Setup SMTP connection with Gmail"""
        try:
            # Use Gmail's SMTP server
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()  # Identify ourselves to smtp gmail client
            smtp.starttls()  # Secure our email with tls encryption
            smtp.ehlo()  # Re-identify ourselves as an encrypted connection
            
            # Login to Gmail
            smtp.login(self.email_address, self.email_password)
            print("Successfully connected to SMTP server")
            return smtp
        except Exception as e:
            print(f"Error setting up SMTP: {str(e)}")
            raise
    
    def create_email_message(self, subject, body, recipient_email, resume_path=None):
        """Create email message with optional attachment"""
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.email_address}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add resume if provided
        if resume_path and os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                resume = MIMEApplication(f.read(), _subtype='pdf')
                resume.add_header('Content-Disposition', 'attachment', filename=os.path.basename(resume_path))
                msg.attach(resume)
        
        return msg
    
    def send_email(self, subject, body, recipient_email, resume_path=None):
        """Send email with retry mechanism"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"\nAttempt {attempt + 1} to send email...")
                
                # Setup SMTP connection
                smtp = self.setup_smtp()
                
                # Create and send message
                msg = self.create_email_message(subject, body, recipient_email, resume_path)
                smtp.send_message(msg)
                
                # Close the connection
                smtp.quit()
                
                print(f"Successfully sent email to {recipient_email}")
                return True
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Email not sent.")
                    return False 