import os
import anthropic
from dotenv import load_dotenv

class ContentEnhancer:
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def enhance_email_content(self, context):
        """Use Anthropic to enhance email content based on company and resume data"""
        company_name = context['company_name']
        company_info = context['company_info']
        resume_analysis = context['resume_analysis']
        
        # Format technical skills
        tech_skills = resume_analysis.get('technicalSkills', {})
        skills_str = ""
        for category, skills in tech_skills.items():
            if isinstance(skills, list):
                skills_str += f"\n- {category}: {', '.join(skills)}"
        
        # Format projects
        projects = resume_analysis.get('keyProjects', [])
        projects_str = "\nKey Projects:"
        for project in projects:
            if isinstance(project, dict):
                projects_str += f"\n- {project.get('name')}: Using {', '.join(project.get('technologies', []))}"
        
        prompt = f"""Create a highly personalized job application email for {company_name} using this information:

Company Details:
- About: {company_info.get('about', 'A leading technology company')}
- Recent News: {company_info.get('recent_news', 'Ongoing innovation')}
- Specialties: {company_info.get('specialties', 'Technology')}
- Industry: {company_info.get('industry', 'Technology')}

My Technical Background:{skills_str}
{projects_str}

Create three paragraphs:
1. Opening: Connect my background with {company_name}'s recent developments ({company_info.get('recent_news')}). Show genuine interest in their mission.
2. Middle: Highlight my most relevant skills and projects that match their specialties ({company_info.get('specialties')}). Include specific examples.
3. Closing: Express enthusiasm for contributing to {company_name}'s specific initiatives and request an interview.

Guidelines:
- Be specific about how my skills match their needs
- Reference their recent work and specialties
- Focus on relevant technical achievements
- Keep it professional but engaging
- Show genuine interest in their specific work

Return ONLY the three paragraphs, separated by newlines."""

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
        - Highlight specific expertise that matches company needs
        
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