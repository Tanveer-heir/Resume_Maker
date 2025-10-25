# 📄 Professional Resume Builder

A modern, feature-rich Flask web application that generates professional PDF resumes with an intuitive interface and database storage for resume history.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎨 **Modern Bootstrap UI** - Clean, responsive design with gradient styling
- 📋 **Comprehensive Resume Sections**
  - Personal Information (Name, Email, Phone, Address)
  - Profile Photo Upload
  - Professional Summary
  - Work Experience
  - Education
  - Technical Skills
  - Projects
  - Certifications
  - Languages
- 📄 **Professional PDF Generation** - Well-formatted PDF resumes with custom styling
- 🖼️ **Photo Integration** - Add profile pictures to your resume
- 💾 **Database Storage** - SQLite database for saving resume history
- 📜 **Resume History** - View and download previously created resumes
- 🎯 **Template Styles** - Choose from Modern, Classic, or Creative templates
- ⚡ **Instant Download** - Generate and download PDF in seconds

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)


## 🎯 Usage

### Creating Your First Resume

1. **Fill in Personal Information**
   - Enter your name, email, phone, and address
   - Upload a profile photo (optional, max 2MB, JPG/PNG)

2. **Add Professional Details**
   - Write a compelling professional summary
   - List your work experience with achievements
   - Add education background
   - Include technical skills and tools

3. **Showcase Projects & Achievements**
   - Describe your key projects
   - Add certifications
   - List languages you speak

4. **Select Template Style**
   - Choose from Modern, Classic, or Creative templates

5. **Generate PDF**
   - Click "Generate Professional Resume PDF"
   - Your resume will download automatically

### Viewing Resume History

- Click **"View Resume History"** to see all previously created resumes
- Download any previous resume with one click


### Key Routes

- `GET /` - Display resume builder form
- `POST /` - Process form and generate PDF
- `GET /history` - View resume history
- `GET /download/<resume_id>` - Download specific resume

## 🎨 Customization

### Adding New Template Styles

Modify the `generate_pdf()` function in `app.py` to create custom PDF layouts based on the `template_style` parameter.

### Modifying Form Fields

Edit the `HTML_TEMPLATE` variable in `app.py` to add or remove form fields. Update the database schema accordingly.

### Styling Changes

The inline CSS in `HTML_TEMPLATE` can be customized to match your preferred color scheme and design.

## 🔒 Security Features

- **File Upload Validation** - Only JPG/PNG files accepted
- **File Size Limits** - Maximum 2MB per photo
- **Secure Filename Handling** - Prevents directory traversal attacks
- **SQL Injection Protection** - Parameterized queries used throughout
- **Input Sanitization** - Form data properly escaped

## 🐛 Troubleshooting


### Deploy to PythonAnywhere

1. Upload files via the Files tab
2. Create a new web app with Flask
3. Set the source code directory
4. Configure WSGI file to import your app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- PDF generation powered by [fpdf2](https://pyfpdf.github.io/fpdf2/)
- UI styled with [Bootstrap 5](https://getbootstrap.com/)

## 📧 Contact
Tanveer Singh 

---

⭐ **Star this repository if you found it helpful!**

