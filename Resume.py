from flask import Flask, request, send_file, Response
from fpdf import FPDF
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # (PDF generation code as before) ...
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Resume", ln=True, align='C')
        
        pdf.set_font("Arial", '', 12)
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        skills = request.form.get("skills")
        
        pdf.cell(0, 10, f"Name: {name}", ln=True)
        pdf.cell(0, 10, f"Email: {email}", ln=True)
        pdf.cell(0, 10, f"Phone: {phone}", ln=True)
        pdf.multi_cell(0, 10, f"Skills:\n{skills}")
        
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_stream = io.BytesIO(pdf_output)
        
        return send_file(pdf_stream, download_name="resume.pdf", as_attachment=True, mimetype='application/pdf')

    with open(os.path.join(os.getcwd(), "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(html_content, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True)
