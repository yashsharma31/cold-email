from email_template import generate_email_content
import json

def test_enhanced_email():
    # Test with a few different companies to see variations
    test_companies = ['Microsoft', 'Tesla', 'Google']
    
    for company in test_companies:
        print(f"\n{'='*80}")
        print(f"Testing email generation for {company}")
        print(f"{'='*80}\n")
        
        # Generate email content
        email_content = generate_email_content(company)
        
        # Print subject
        print("Subject:")
        print("-" * 40)
        print(email_content['subject'])
        print("\nBody:")
        print("-" * 40)
        print(email_content['body'])
        
        print("\nWaiting for next company...\n")
        input("Press Enter to continue...")

if __name__ == "__main__":
    print("Testing Enhanced Email Generation with Anthropic\n")
    test_enhanced_email() 