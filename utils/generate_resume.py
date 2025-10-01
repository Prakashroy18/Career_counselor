from fpdf import FPDF
import os
import uuid

def generate_resume(
    name, email, phone, location, career_objective, education,
    technical_skills, non_technical_skills, projects, mini_projects,
    internships, achievements, workshops, languages, career_path
):
    # Sanitize all text fields
    name = sanitize_text(name)
    email = sanitize_text(email)
    phone = sanitize_text(phone)
    location = sanitize_text(location)
    career_objective = sanitize_text(career_objective)
    education = sanitize_dict(education)
    technical_skills = [sanitize_text(s) for s in technical_skills]
    non_technical_skills = [sanitize_text(s) for s in non_technical_skills]
    projects = [sanitize_text(s) for s in projects]
    mini_projects = [sanitize_text(s) for s in mini_projects]
    internships = [sanitize_text(s) for s in internships]
    achievements = [sanitize_text(s) for s in achievements]
    workshops = [sanitize_text(s) for s in workshops]
    languages = [sanitize_text(s) for s in languages]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    # Fonts
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, name.upper(), ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"{phone} | {email} | Location: {location}", ln=True)
    pdf.cell(0, 10, f"Career Path: {career_path}", ln=True)

    # Career Objective
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Career Objective", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, career_objective)

    # Education
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"B.Tech, {education['btech']['college']} ({education['btech']['duration']})", ln=True)
    pdf.cell(0, 10, f"CGPA: {education['btech']['cgpa']}/10", ln=True)
    pdf.cell(0, 10, f"Intermediate, {education['inter']['college']} ({education['inter']['duration']})", ln=True)
    pdf.cell(0, 10, f"Percentage: {education['inter']['percentage']}%", ln=True)
    pdf.cell(0, 10, f"SSC, {education['ssc']['school']} ({education['ssc']['duration']})", ln=True)
    pdf.cell(0, 10, f"Percentage: {education['ssc']['percentage']}%", ln=True)

    # Technical Skills
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Technical Skills", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, "- " + "\n- ".join(technical_skills))

    # Non-Technical Skills
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Non-Technical Skills", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, ", ".join(non_technical_skills))

    # Projects
    if projects:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Projects", ln=True)
        pdf.set_font("Arial", '', 11)
        for proj in projects:
            pdf.multi_cell(0, 10, f"- {proj}")

    # Mini Projects
    if mini_projects:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Mini/Community Projects", ln=True)
        pdf.set_font("Arial", '', 11)
        for proj in mini_projects:
            pdf.multi_cell(0, 10, f"- {proj}")

    # Internships
    if internships:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Internships", ln=True)
        pdf.set_font("Arial", '', 11)
        for intern in internships:
            pdf.multi_cell(0, 10, f"- {intern}")

    # Achievements
    if achievements:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Achievements & Certifications", ln=True)
        pdf.set_font("Arial", '', 11)
        for ach in achievements:
            pdf.multi_cell(0, 10, f"- {ach}")

    # Workshops
    if workshops:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Workshops & Volunteering", ln=True)
        pdf.set_font("Arial", '', 11)
        for work in workshops:
            pdf.multi_cell(0, 10, f"- {work}")

    # Languages
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Languages", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, ", ".join(languages))

    # Declaration
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Declaration", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, "I hereby declare that the information provided above is true to the best of my knowledge.")
    pdf.cell(0, 10, f"Place: {location}", ln=True)
    pdf.cell(0, 10, f"Signature: {name.split()[0][0]}. {name.split()[-1]}", ln=True)

    # Save
    output_dir = "generated_resumes"
    os.makedirs(output_dir, exist_ok=True)
    unique_id = uuid.uuid4().hex[:8]
    pdf_path = os.path.join('generated_resumes', f"{name.replace(' ', '_')}_{unique_id}.pdf")
    pdf.output(pdf_path)
    return pdf_path

def sanitize_text(text):
    # Replace EN DASH and EM DASH with a regular hyphen
    if isinstance(text, str):
        return text.replace("–", "-").replace("—", "-")
    return text

def sanitize_dict(d):
    # Recursively sanitize all strings in a dict
    if isinstance(d, dict):
        return {k: sanitize_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [sanitize_dict(x) for x in d]
    else:
        return sanitize_text(d)
