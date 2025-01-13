import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from PyPDF2 import PdfReader

class ResumeAnalyzer:
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.cache_file = 'resume_analysis.json'
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def extract_resume_info(self, resume_text):
        """Extract key information from resume using Anthropic"""
        prompt = f"""Analyze this resume content and extract key information in a structured format:

        Resume Content:
        {resume_text}

        Please extract and organize the following information:
        1. Technical Skills (grouped by category: languages, frameworks, tools, etc.)
        2. Key Projects (with technologies used and impact metrics)
        3. Core Competencies (e.g., system design, architecture, team leadership)
        4. Notable Achievements (with quantifiable metrics)
        5. Industry Experience (domains worked in)
        6. Keywords (important terms for matching with job descriptions)

        Format the response as a structured JSON object with these categories.
        Focus on technical and quantifiable aspects that would be relevant for software engineering positions.
        Include specific metrics and technologies wherever possible.
        
        Guidelines:
        - Extract actual information from the resume, don't make assumptions
        - Focus on concrete skills and achievements
        - Include all relevant technologies mentioned
        - Preserve any metrics or numbers mentioned
        - Group similar skills together
        - Include both technical and soft skills
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                temperature=0.1,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            try:
                # Try to parse as JSON directly
                resume_data = json.loads(content)
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON portion
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    resume_data = json.loads(content[start:end])
                else:
                    raise ValueError("Could not extract valid JSON from response")
            
            return resume_data
            
        except Exception as e:
            print(f"Error analyzing resume: {str(e)}")
            return None
    
    def cache_analysis(self, analysis):
        """Cache the resume analysis to a file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"Resume analysis cached to {self.cache_file}")
        except Exception as e:
            print(f"Error caching analysis: {str(e)}")
    
    def load_cached_analysis(self):
        """Load cached resume analysis"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cached analysis: {str(e)}")
        return None
    
    def get_resume_analysis(self, force_refresh=False):
        """Get resume analysis, using cache if available"""
        if not force_refresh:
            cached = self.load_cached_analysis()
            if cached:
                return cached
        
        # Read resume content
        resume_path = 'Yash-Sharma-Resume.pdf'
        if not os.path.exists(resume_path):
            print(f"Error: Resume file not found at {resume_path}")
            return None
        
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(resume_path)
        if not resume_text:
            return None
        
        # Extract and cache analysis
        analysis = self.extract_resume_info(resume_text)
        if analysis:
            self.cache_analysis(analysis)
        return analysis

def get_formatted_resume_highlights(analysis):
    """Format resume analysis into a string for email generation"""
    if not analysis:
        return ""
    
    highlights = []
    
    # Add technical skills
    if 'Technical Skills' in analysis:
        highlights.append("Technical Expertise:")
        for category, skills in analysis['Technical Skills'].items():
            if isinstance(skills, list):
                highlights.append(f"- {category}: {', '.join(skills)}")
            else:
                highlights.append(f"- {category}: {skills}")
    
    # Add key projects
    if 'Key Projects' in analysis:
        highlights.append("\nSignificant Projects:")
        for project in analysis['Key Projects']:
            if isinstance(project, dict):
                highlights.append(f"- {project.get('name', 'Project')}: {project.get('description', '')}")
                if 'impact' in project:
                    highlights.append(f"  Impact: {project['impact']}")
            else:
                highlights.append(f"- {project}")
    
    # Add achievements
    if 'Notable Achievements' in analysis:
        highlights.append("\nKey Achievements:")
        for achievement in analysis['Notable Achievements']:
            highlights.append(f"- {achievement}")
    
    # Add core competencies
    if 'Core Competencies' in analysis:
        highlights.append("\nCore Competencies:")
        for competency in analysis['Core Competencies']:
            highlights.append(f"- {competency}")
    
    # Add industry experience
    if 'Industry Experience' in analysis:
        highlights.append("\nIndustry Experience:")
        for industry in analysis['Industry Experience']:
            highlights.append(f"- {industry}")
    
    return "\n".join(highlights) 