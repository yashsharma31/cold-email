from linkedin_info import get_company_info
from anthropic_helper import ContentEnhancer

# Initialize the content enhancer
content_enhancer = ContentEnhancer()

def get_resume_highlights():
    """Get key highlights from resume"""
    return """
    Technical Skills:
    - Proficient in Python, JavaScript, React, Node.js
    - Experience with cloud platforms (AWS, GCP)
    - Strong background in system design and architecture
    
    Recent Projects:
    - Led development of scalable microservices architecture
    - Implemented AI/ML solutions for data processing
    - Built high-performance web applications
    
    Achievements:
    - Reduced system response time by 40%
    - Implemented automated testing, improving coverage by 75%
    - Led team of 5 developers on critical projects
    """

def generate_email_content(company_name):
    # Get enhanced company information
    company_info = get_company_info(company_name)
    company_info['company_name'] = company_name  # Add company name to info dict
    
    # Get resume highlights
    resume_data = get_resume_highlights()
    
    # Generate enhanced content using Anthropic
    enhanced_content = content_enhancer.enhance_email_content(company_info, resume_data)
    
    # Generate subject line
    subject = content_enhancer.generate_subject_line(
        company_name,
        "Software Engineer",
        company_info['specialties']
    )
    
    # If Anthropic enhancement fails, use fallback template
    if not enhanced_content:
        return generate_fallback_content(company_name, company_info)
    
    # Create the email body using enhanced content
    body = f"""Dear Hiring Manager at {company_name},

{enhanced_content['opening']}

{enhanced_content['middle']}

{enhanced_content['closing']}

Best regards,
Yash Sharma"""

    return {
        "subject": subject,
        "body": body
    }

def generate_fallback_content(company_name, company_info):
    """Fallback template if Anthropic enhancement fails"""
    specialties = company_info['specialties']
    recent_news = company_info['recent_news']
    industry = company_info['industry']
    about = company_info['about']
    
    subject = f"Software Engineer Position at {company_name} - Experienced in {specialties.split(', ')[0]}"
    
    body = f"""Dear Hiring Manager at {company_name},

I hope this email finds you well. I am writing to express my strong interest in the Software Engineer position at {company_name}. As {about}, your company's {recent_news} has particularly caught my attention, and I'm excited about the possibility of contributing to your continued innovation.

What specifically draws me to {company_name} is your focus on {specialties}. My background in software development, with hands-on experience in these areas, aligns perfectly with your technical requirements. I'm particularly interested in how {company_name} is shaping the future of {industry} through innovative solutions.

Key highlights from my experience that align with your needs:
• Developed scalable applications using modern technology stacks, particularly in {specialties.split(', ')[0]}
• Led technical projects involving {specialties.split(', ')[1] if ', ' in specialties else specialties}
• Implemented efficient solutions for complex technical challenges
• Strong background in {specialties}

I have attached my resume for your review, which details my technical expertise and project experiences. I would welcome the opportunity to discuss how my background in {specialties.split(', ')[0]} could contribute to {company_name}'s continued success in {industry}.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team's ongoing {recent_news}.

Best regards,
Yash Sharma"""

    return {
        "subject": subject,
        "body": body
    } 