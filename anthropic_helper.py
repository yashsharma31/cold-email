import os
import anthropic
from dotenv import load_dotenv

class ContentEnhancer:
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def enhance_email_content(self, company_info, resume_data):
        """Use Anthropic to enhance email content based on company and resume data"""
        prompt = f"""You are an expert in crafting personalized job application emails. Create highly tailored content for an email 
        to {company_info['company_name']} using the following information:

        Company Information:
        - About: {company_info['about']}
        - Recent News: {company_info['recent_news']}
        - Specialties: {company_info['specialties']}
        - Industry: {company_info['industry']}

        Resume Highlights:
        {resume_data}

        Create three distinct paragraphs (separated by double newlines):

        1. Opening: A compelling first paragraph that connects my background with the company's recent developments and shows genuine interest in their mission.

        2. Experience: A focused paragraph highlighting 2-3 most relevant experiences and skills that directly match their specialties and needs.

        3. Closing: A strong final paragraph emphasizing specific contributions I could make and expressing enthusiasm for next steps.

        Guidelines:
        - Be professional but conversational
        - Show deep knowledge of the company's work
        - Focus on specific contributions, not generic statements
        - Keep each paragraph concise (3-4 sentences max)
        - Don't include salutation or signature
        - Separate paragraphs with double newlines
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract the content and split into paragraphs
            content = response.content[0].text.strip()
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            if len(paragraphs) >= 3:
                return {
                    'opening': paragraphs[0],
                    'middle': paragraphs[1],
                    'closing': paragraphs[2]
                }
            else:
                print("Error: Not enough paragraphs generated")
                return None
            
        except Exception as e:
            print(f"Error generating enhanced content: {str(e)}")
            return None
    
    def generate_subject_line(self, company_name, role, specialties):
        """Generate an attention-grabbing subject line"""
        prompt = f"""Create a compelling subject line for a job application email to {company_name} for a {role} position.
        The company specializes in: {specialties}

        Requirements:
        - Must be attention-grabbing but professional
        - Include both the role and a key relevant skill/technology
        - Maximum 8-10 words
        - Don't use generic phrases like "applying for position"
        - Focus on value proposition
        
        Return ONLY the subject line, nothing else."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=100,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"Error generating subject line: {str(e)}")
            return f"Software Engineer Position at {company_name} - Experienced in {specialties.split(', ')[0]}" 