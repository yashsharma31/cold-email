from linkedin_auth import LinkedInAuth
import time

class CompanyInfoManager:
    def __init__(self):
        self.linkedin = None
        self.cached_info = {
            'Microsoft': {
                'recent_news': 'advancement in AI and cloud computing solutions',
                'specialties': 'cloud computing, artificial intelligence, enterprise software',
                'industry': 'Technology',
                'about': 'Leading provider of cloud computing, AI, and enterprise software solutions'
            },
            'Google': {
                'recent_news': 'developments in machine learning and AI research',
                'specialties': 'search technology, cloud computing, artificial intelligence',
                'industry': 'Technology',
                'about': 'Global technology leader in search, cloud computing, and AI research'
            },
            'Apple': {
                'recent_news': 'innovations in hardware and software integration',
                'specialties': 'consumer electronics, software development, design',
                'industry': 'Technology',
                'about': 'Pioneer in consumer electronics, software, and services'
            },
            'Tesla': {
                'recent_news': 'advancements in electric vehicles and sustainable energy',
                'specialties': 'electric vehicles, renewable energy, autonomous driving',
                'industry': 'Automotive & Energy',
                'about': 'Leading innovator in electric vehicles and sustainable energy solutions'
            },
            'Nvidia': {
                'recent_news': 'breakthroughs in GPU technology and AI computing',
                'specialties': 'GPU technology, AI computing, gaming technology',
                'industry': 'Technology',
                'about': 'Pioneer in GPU technology and AI computing solutions'
            },
            'Salesforce': {
                'recent_news': 'innovations in CRM and cloud solutions',
                'specialties': 'CRM software, cloud computing, enterprise solutions',
                'industry': 'Software',
                'about': 'Leading provider of CRM and enterprise cloud solutions'
            },
            'HP': {
                'recent_news': 'innovations in printing and computing technology',
                'specialties': 'computing hardware, printing solutions, enterprise IT',
                'industry': 'Technology',
                'about': 'Global leader in personal computing and printing solutions'
            },
            'Dell': {
                'recent_news': 'advancements in enterprise solutions and computing',
                'specialties': 'enterprise computing, IT solutions, cloud infrastructure',
                'industry': 'Technology',
                'about': 'Provider of enterprise computing solutions and personal technology'
            },
            'Adobe': {
                'recent_news': 'innovations in creative software and digital experiences',
                'specialties': 'creative software, digital media, enterprise solutions',
                'industry': 'Software',
                'about': 'Leader in creative software and digital experience solutions'
            },
            'Intel': {
                'recent_news': 'developments in semiconductor technology and AI',
                'specialties': 'semiconductor design, processor technology, AI acceleration',
                'industry': 'Technology',
                'about': 'Pioneer in semiconductor technology and computing innovation'
            }
        }
    
    def initialize_linkedin(self):
        """Initialize LinkedIn connection if not already done"""
        if not self.linkedin:
            self.linkedin = LinkedInAuth()
            return self.linkedin.login()
        return True
    
    def merge_company_info(self, cached_info, linkedin_info):
        """Merge cached and LinkedIn info, preferring LinkedIn data when available"""
        merged = cached_info.copy()
        if linkedin_info:
            for key, value in linkedin_info.items():
                if value:  # Only update if LinkedIn provided a value
                    merged[key] = value
        return merged
    
    def get_company_info(self, company_name):
        """Get company information, combining cached and LinkedIn data"""
        # Get cached info
        cached_info = self.cached_info.get(company_name, {
            'recent_news': 'continuous growth and innovation',
            'specialties': 'technology and innovation',
            'industry': 'Technology',
            'about': 'Leading technology company'
        })
        
        # Try to get LinkedIn data
        linkedin_info = None
        try:
            if self.initialize_linkedin():
                linkedin_info = self.linkedin.get_company_page(company_name)
        except Exception as e:
            print(f"Error getting LinkedIn data: {str(e)}")
        
        # Merge the information
        return self.merge_company_info(cached_info, linkedin_info)
    
    def __del__(self):
        """Cleanup"""
        if self.linkedin:
            self.linkedin.close()

# Create a singleton instance
_company_manager = CompanyInfoManager()

def get_company_info(company_name):
    """Public interface to get company information"""
    return _company_manager.get_company_info(company_name) 