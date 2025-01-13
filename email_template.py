from linkedin_info import get_company_info
from anthropic_helper import ContentEnhancer
from resume_analyzer import ResumeAnalyzer, get_formatted_resume_highlights

# Initialize the content enhancer and resume analyzer
content_enhancer = ContentEnhancer()
resume_analyzer = ResumeAnalyzer()

def generate_email_content(company_name):
    try:
        # Get enhanced company information
        company_info = get_company_info(company_name)
        if not company_info:
            company_info = {
                'about': 'a leading technology company',
                'recent_news': 'ongoing innovation',
                'specialties': 'technology',
                'industry': 'technology'
            }
        company_info['company_name'] = company_name
        
        # Try to get resume analysis
        resume_analyzer = ResumeAnalyzer()
        resume_analysis = resume_analyzer.get_resume_analysis()
        
        if not resume_analysis:
            return generate_fallback_content(company_name, company_info)
            
        # Create enhanced content
        enhanced_content = content_enhancer.enhance_email_content({
            'company_name': company_name,
            'company_info': company_info,
            'resume_analysis': resume_analysis
        })
        
        if not enhanced_content:
            return generate_fallback_content(company_name, company_info)
            
        # Generate subject line
        subject = content_enhancer.generate_subject_line(
            company_name,
            "Software Engineer",
            company_info['specialties']
        )
        
        if not subject:
            subject = f"Software Engineer Position at {company_name} - Full Stack Developer with Cloud Expertise"
        
        # Create the email body
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
        
    except Exception as e:
        print(f"Error generating email content: {str(e)}")
        return generate_fallback_content(company_name, company_info)

def generate_fallback_content(company_name, company_info):
    """Fallback template if Anthropic enhancement fails"""
    specialties = company_info.get('specialties', 'technology')
    recent_news = company_info.get('recent_news', 'ongoing innovation')
    industry = company_info.get('industry', 'technology')
    about = company_info.get('about', 'a leading technology company')
    
    subject = f"Software Engineer Position at {company_name} - Full Stack Developer with Cloud Expertise"
    
    body = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the Software Engineer position at {company_name}. With extensive experience in full-stack development, cloud computing, and modern web technologies, I am excited about the opportunity to contribute to {company_name}'s innovative work in {industry}.

My technical expertise includes:
• Frontend: React.js, Next.js, TypeScript, and modern UI frameworks
• Backend: Python, Node.js, and cloud services (AWS, Firebase)
• DevOps: CI/CD pipelines, Docker, and infrastructure automation
• Additional: WebGL, SVG optimization, and performance tuning

What particularly draws me to {company_name} is your focus on {specialties}. I have hands-on experience building scalable applications and implementing efficient solutions for complex technical challenges. Your recent work on {recent_news} aligns perfectly with my interest in pushing technological boundaries while maintaining high performance and reliability standards.

I would welcome the opportunity to discuss how my technical background and passion for innovation could contribute to {company_name}'s continued success. I have attached my resume for your review, which provides more detail about my projects and achievements.

Thank you for considering my application. I look forward to the possibility of joining your team and contributing to {company_name}'s mission.

Best regards,
Yash Sharma"""

    return {
        "subject": subject,
        "body": body
    } 