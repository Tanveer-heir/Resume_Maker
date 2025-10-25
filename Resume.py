from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
from fpdf import FPDF
import io
import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT,
                  address TEXT,
                  summary TEXT,
                  experience TEXT,
                  education TEXT,
                  skills TEXT,
                  certifications TEXT,
                  projects TEXT,
                  languages TEXT,
                  template_style TEXT,
                  photo_path TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

class EnhancedPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Professional Resume', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.ln(2)
        
        self.set_font('Arial', '', 11)
        if content:
            # Handle multi-line content
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    self.cell(0, 6, line.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
        self.ln(5)

    def add_photo(self, photo_path):
        if photo_path and os.path.exists(photo_path):
            try:
                self.image(photo_path, 160, 30, 30, 40)
            except:
                pass  # Skip if image can't be processed

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename = secure_filename(file.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(photo_path)

        # Collect form data
        form_data = {
            'name': request.form.get("name", ""),
            'email': request.form.get("email", ""),
            'phone': request.form.get("phone", ""),
            'address': request.form.get("address", ""),
            'summary': request.form.get("summary", ""),
            'experience': request.form.get("experience", ""),
            'education': request.form.get("education", ""),
            'skills': request.form.get("skills", ""),
            'certifications': request.form.get("certifications", ""),
            'projects': request.form.get("projects", ""),
            'languages': request.form.get("languages", ""),
            'template_style': request.form.get("template_style", "modern")
        }

        # Save to database
        try:
            conn = sqlite3.connect('resumes.db')
            c = conn.cursor()
            c.execute('''INSERT INTO resumes 
                        (name, email, phone, address, summary, experience, education, 
                         skills, certifications, projects, languages, template_style, photo_path)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (form_data['name'], form_data['email'], form_data['phone'], 
                      form_data['address'], form_data['summary'], form_data['experience'],
                      form_data['education'], form_data['skills'], form_data['certifications'],
                      form_data['projects'], form_data['languages'], form_data['template_style'], photo_path))
            conn.commit()
            conn.close()
            flash('Resume data saved successfully!', 'success')
        except Exception as e:
            flash(f'Error saving data: {str(e)}', 'error')

        # Generate PDF
        return generate_pdf(form_data, photo_path)

    return render_template_string(HTML_TEMPLATE)

def generate_pdf(data, photo_path):
    pdf = EnhancedPDF()
    pdf.add_page()
    
    # Add photo if available
    if photo_path:
        pdf.add_photo(photo_path)
    
    # Header with contact info
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, data['name'], ln=True, align='L')
    
    pdf.set_font("Arial", '', 11)
    contact_info = f"Email: {data['email']} | Phone: {data['phone']}"
    if data['address']:
        contact_info += f" | Address: {data['address']}"
    pdf.cell(0, 8, contact_info, ln=True)
    pdf.ln(10)
    
    # Professional Summary
    if data['summary']:
        pdf.add_section("PROFESSIONAL SUMMARY", data['summary'])
    
    # Experience
    if data['experience']:
        pdf.add_section("WORK EXPERIENCE", data['experience'])
    
    # Education
    if data['education']:
        pdf.add_section("EDUCATION", data['education'])
    
    # Skills
    if data['skills']:
        pdf.add_section("TECHNICAL SKILLS", data['skills'])
    
    # Projects
    if data['projects']:
        pdf.add_section("PROJECTS", data['projects'])
    
    # Certifications
    if data['certifications']:
        pdf.add_section("CERTIFICATIONS", data['certifications'])
    
    # Languages
    if data['languages']:
        pdf.add_section("LANGUAGES", data['languages'])
    
    # Generate PDF
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_stream = io.BytesIO(pdf_output)
    
    return send_file(pdf_stream, download_name=f"{data['name']}_resume.pdf", 
                    as_attachment=True, mimetype='application/pdf')

@app.route("/history")
def history():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email, created_at FROM resumes ORDER BY created_at DESC LIMIT 10')
    resumes = c.fetchall()
    conn.close()
    
    history_html = """
    <h2>Resume History</h2>
    <table border="1" style="width:100%; border-collapse: collapse;">
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Created</th><th>Action</th></tr>
    """
    for resume in resumes:
        history_html += f"""
        <tr>
            <td>{resume[0]}</td>
            <td>{resume[1]}</td>
            <td>{resume[2]}</td>
            <td>{resume[3]}</td>
            <td><a href="/download/{resume[0]}">Download PDF</a></td>
        </tr>
        """
    history_html += "</table><br><a href='/'>Back to Form</a>"
    
    return history_html

@app.route("/download/<int:resume_id>")
def download_resume(resume_id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
    resume = c.fetchone()
    conn.close()
    
    if not resume:
        flash('Resume not found!', 'error')
        return redirect(url_for('index'))
    
    data = {
        'name': resume[1],
        'email': resume[2],
        'phone': resume[3] or '',
        'address': resume[4] or '',
        'summary': resume[5] or '',
        'experience': resume[6] or '',
        'education': resume[7] or '',
        'skills': resume[8] or '',
        'certifications': resume[9] or '',
        'projects': resume[10] or '',
        'languages': resume[11] or '',
        'template_style': resume[12] or 'modern'
    }
    
    return generate_pdf(data, resume[13])  

# Enhanced HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Resume Builder</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .form-container { 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            margin: 20px auto;
            max-width: 800px;
        }
        .section-header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0 15px 0;
        }
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px 30px;
            font-weight: bold;
        }
        .btn-primary:hover {
            background: linear-gradient(45deg, #5a6fd8, #6a42a0);
        }
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="form-container p-4">
            <h1 class="text-center mb-4" style="color: #667eea;">🚀 Professional Resume Builder</h1>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="post" enctype="multipart/form-data">
                <!-- Personal Information -->
                <div class="section-header">
                    <h3>📋 Personal Information</h3>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Full Name *</label>
                        <input type="text" class="form-control" name="name" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Email Address *</label>
                        <input type="email" class="form-control" name="email" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Phone Number</label>
                        <input type="tel" class="form-control" name="phone">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Address</label>
                        <input type="text" class="form-control" name="address">
                    </div>
                    <div class="col-12 mb-3">
                        <label class="form-label">Profile Photo (Optional)</label>
                        <input type="file" class="form-control" name="photo" accept=".jpg,.jpeg,.png">
                        <small class="text-muted">Max 2MB, JPG/PNG format</small>
                    </div>
                </div>

                <!-- Professional Summary -->
                <div class="section-header">
                    <h3>💼 Professional Summary</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="summary" rows="4" 
                              placeholder="Brief overview of your professional background, key achievements, and career objectives..."></textarea>
                </div>

                <!-- Work Experience -->
                <div class="section-header">
                    <h3>🏢 Work Experience</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="experience" rows="6" 
                              placeholder="Job Title - Company Name (Start Date - End Date)
• Key responsibility or achievement
• Another key responsibility or achievement
• Quantified achievement with numbers/percentages

Job Title - Company Name (Start Date - End Date)
• Key responsibility or achievement"></textarea>
                </div>

                <!-- Education -->
                <div class="section-header">
                    <h3>🎓 Education</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="education" rows="4" 
                              placeholder="Degree - University/Institution (Year)
• Relevant coursework, GPA (if strong), honors, etc.

Certification - Institution (Year)"></textarea>
                </div>

                <!-- Technical Skills -->
                <div class="section-header">
                    <h3>⚡ Technical Skills</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="skills" rows="4" 
                              placeholder="Programming Languages: Python, JavaScript, Java
Frameworks: Django, Flask, React, Node.js
Databases: PostgreSQL, MongoDB, MySQL
Tools: Git, Docker, AWS, Linux"></textarea>
                </div>

                <!-- Projects -->
                <div class="section-header">
                    <h3>🚀 Projects</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="projects" rows="5" 
                              placeholder="Project Name - Brief Description
• Technology stack used
• Key features implemented
• Results/impact (if applicable)
• GitHub link or live demo (if available)"></textarea>
                </div>

                <!-- Certifications -->
                <div class="section-header">
                    <h3>🏆 Certifications</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="certifications" rows="3" 
                              placeholder="AWS Certified Developer (2024)
Python Institute PCAP Certification (2023)
Google Cloud Professional (2024)"></textarea>
                </div>

                <!-- Languages -->
                <div class="section-header">
                    <h3>🌍 Languages</h3>
                </div>
                <div class="mb-3">
                    <textarea class="form-control" name="languages" rows="2" 
                              placeholder="English (Native/Fluent)
Spanish (Conversational)
French (Basic)"></textarea>
                </div>

                <!-- Template Style -->
                <div class="section-header">
                    <h3>🎨 Template Style</h3>
                </div>
                <div class="mb-4">
                    <select class="form-control" name="template_style">
                        <option value="modern">Modern (Clean & Professional)</option>
                        <option value="classic">Classic (Traditional)</option>
                        <option value="creative">Creative (Designer-Friendly)</option>
                    </select>
                </div>

                <div class="text-center">
                    <button type="submit" class="btn btn-primary btn-lg">
                        📄 Generate Professional Resume PDF
                    </button>
                </div>
            </form>
            
            <div class="text-center mt-4">
                <a href="/history" class="btn btn-outline-secondary">View Resume History</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
