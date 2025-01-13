from linkedin_auth import LinkedInAuth
import time

def test_linkedin_auth():
    print("Testing LinkedIn Authentication...")
    
    # Initialize LinkedIn authentication
    linkedin = LinkedInAuth()
    
    # Try to login
    if linkedin.login():
        print("\nSuccessfully logged in!")
        
        # Test with a few companies
        test_companies = ['Microsoft', 'Google', 'Tesla']
        
        for company in test_companies:
            print(f"\nFetching information for {company}...")
            company_info = linkedin.get_company_page(company)
            
            print(f"\n{company} Information:")
            print("=" * 50)
            for key, value in company_info.items():
                if value:
                    print(f"{key.capitalize()}: {value}")
            print("=" * 50)
            
            # Wait a bit between requests
            time.sleep(2)
        
        # Close the browser
        linkedin.close()
        print("\nTest completed successfully!")
    else:
        print("Failed to log in to LinkedIn. Please check your credentials.")

if __name__ == "__main__":
    test_linkedin_auth() 