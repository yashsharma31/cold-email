def generate_email_content(company_name):
    subject = f"Job Application - Software Engineer Position at {company_name}"
    
    body = f"""Dear Hiring Manager at {company_name},

I hope this email finds you well. I am writing to express my strong interest in the Software Engineer position at {company_name}. With my strong background in software development and passion for technology, I believe I would be a valuable addition to your team.

I am particularly drawn to {company_name}'s innovative approach to technology and its commitment to excellence. My experience in full-stack development, cloud computing, and agile methodologies aligns well with your company's technical requirements.

I have attached my resume for your review. I would welcome the opportunity to discuss how my skills and experience could contribute to {company_name}'s continued success.

Thank you for considering my application.

Best regards,
[Your Name]"""

    return {
        "subject": subject,
        "body": body
    } 