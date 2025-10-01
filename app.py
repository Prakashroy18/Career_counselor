from flask import Flask, render_template, request, redirect, url_for, send_file
from utils.generate_resume import generate_resume
import joblib
import os

app = Flask(__name__)

# Load ML model and encoder
model = joblib.load("model/career_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session_data = request.form.to_dict(flat=False)
        return render_template('result.html', data=session_data)
    return render_template('form.html')

@app.route('/result', methods=['POST'])

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form

    # Personal & Academic Info
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    location = data.get("location")
    career_objective = data.get("career_objective")
    cgpa = float(data.get("cgpa"))
    marks_12 = float(data.get("marks_12"))
    marks_10 = float(data.get("marks_10"))
    education = data.get("education")
    school_10 = data.get("school_10")
    college_12 = data.get("college_12")
    grad_college = data.get("grad_college")
    pg_college = data.get("pg_college")

    # Projects
    project_title_1 = data.get("project_title_1")
    project_details_1 = data.get("project_details_1")
    project_title_2 = data.get("project_title_2")
    project_details_2 = data.get("project_details_2")

    # Internships
    internship_1 = data.get("internship_1")
    internship_1_details = data.get("internship_1_details")
    internship_2 = data.get("internship_2")
    internship_2_details = data.get("internship_2_details")

    # Skills and Extras
    skills = [s.strip() for s in data.get("skills", "").split(",")]
    non_technical = [s.strip() for s in data.get("non_technical", "").split(",")]
    interests = [s.strip() for s in data.get("interests", "").split(",")]
    work_type = data.get("work_type")
    generate_resume_flag = "generate_resume" in data

    # Prepare input for model (combine relevant fields)
    combined_skills = ', '.join(skills + interests)
    input_text = f"{education} {combined_skills} {work_type}"

    # Preprocess and predict
    input_vec = label_encoder.transform([input_text])
    prediction = model.predict(input_vec)
    career = prediction

    # Prepare projects and internships for resume
    projects = []
    if project_title_1 or project_details_1:
        projects.append(f"{project_title_1}: {project_details_1}")
    if project_title_2 or project_details_2:
        projects.append(f"{project_title_2}: {project_details_2}")

    internships = []
    if internship_1 or internship_1_details:
        internships.append(f"{internship_1}: {internship_1_details}")
    if internship_2 or internship_2_details:
        internships.append(f"{internship_2}: {internship_2_details}")

    # Generate resume if selected
    resume_file = None
    resume_filename = None
    if generate_resume_flag:
        resume_file = generate_resume(
            name, email, phone, location, career_objective,
            {
                "btech": {"college": grad_college, "duration": "2022–2026", "cgpa": cgpa},
                "inter": {"college": college_12, "duration": "2020–2022", "percentage": marks_12},
                "ssc": {"school": school_10, "duration": "2019–2020", "percentage": marks_10},
                "pg": {"college": pg_college, "duration": "", "cgpa": ""}
            },
            skills, non_technical,
            projects,
            [],  # miniprojects
            internships,
            [],  # achievements
            [],  # workshops
            ["English", "Telugu", "Hindi"],
            str(career[0]) if isinstance(career, (list, tuple)) else str(career)  # ensure string for career_path
        )
        resume_filename = os.path.basename(resume_file)


    return render_template(
        "result.html",
        name=name,
        career=career,
        resume_filename=resume_filename
    )

def result():
    form = request.form
    name = form['name']
    email = form['email']
    phone = form['phone']
    location = form['location']
    career_objective = form['career_objective']
    skills = form.getlist('skills')
    interests = form.getlist('interests')
    personality = form['personality']
    education = form['education']
    work_type = form['work_type']

    # Combine and predict
    input_text = f"{education} {', '.join(skills + interests)} {personality} {work_type}"
    prediction = model.predict([input_text])[0]
    career = label_encoder.inverse_transform([prediction])[0]

    # Generate resume if requested
    
    if 'generate_resume' in form:
        resume_path = generate_resume(name, email, phone, location, career_objective, career)
        resume_filename = os.path.basename(resume_path)
        return render_template('result.html', career=career, resume_filename=resume_filename)

    return render_template('result.html', career=career)

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/roadmap-doctor')
def roadmap_doctor():
    # This renders your dedicated doctor roadmap page
    return render_template('roadmap-doctor.html')

@app.route('/roadmap-carrer')
def roadmap_carrer():
    career = request.args.get('career', 'engineering')
    return render_template('roadmap-carrer.html', career=career)

@app.route('/download_resume/<filename>')
def download_resume(filename):
    file_path = os.path.join('generated_resumes', filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pdf', as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
