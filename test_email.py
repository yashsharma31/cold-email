import os
from dotenv import load_dotenv
from email_template import generate_email_content
from resume_analyzer import ResumeAnalyzer
from email_sender import EmailSender
import json

def test_complete_email_flow():
    print("\n=== Testing Complete Email Flow ===\n")
    
    # 1. Test Resume Analysis
    print("Step 1: Analyzing Resume...")
    analyzer = ResumeAnalyzer()
    analysis = analyzer.get_resume_analysis(force_refresh=True)
    
    if not analysis:
        print("Failed to analyze resume")
        return
    
    print("\nResume Analysis Complete!")
    print("Found skills in categories:", ", ".join(analysis.get("technicalSkills", {}).keys()))
    
    # 2. Generate Enhanced Email
    print("\nStep 2: Generating Enhanced Email...")
    test_company = "Microsoft"  # Using Microsoft as a test case
    email_content = generate_email_content(test_company)
    
    # 3. Display Generated Email
    print("\n=== Generated Email ===\n")
    print("To:", test_company)
    print("Subject:", email_content["subject"])
    print("\nBody:\n")
    print(email_content["body"])
    
    # 4. Test Email Sending
    print("\nStep 3: Testing Email Sending...")
    try:
        sender = EmailSender()
        test_recipient = "yash.sh0031@gmail.com"  # Your email for testing
        
        print(f"\nSending test email to: {test_recipient}")
        success = sender.send_email(
            subject=email_content["subject"],
            body=email_content["body"],
            recipient_email=test_recipient,
            resume_path="Yash-Sharma-Resume.pdf"
        )
        
        if success:
            print("\nTest email sent successfully!")
        else:
            print("\nFailed to send test email")
            
    except Exception as e:
        print(f"\nError during email sending: {str(e)}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    load_dotenv()
    
    # Check for required environment variables
    missing_vars = []
    for var in ["ANTHROPIC_API_KEY", "EMAIL_ADDRESS", "EMAIL_PASSWORD"]:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Error: Missing required environment variables:", ", ".join(missing_vars))
    else:
        test_complete_email_flow() 