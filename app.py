from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Max Upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")  # Multiple files receive panrathuku
        image_paths = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_paths.append(file_path)

        # Convert to PDF
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'document.pdf')
        create_pdf(image_paths, pdf_path)
        return send_from_directory(directory=os.path.dirname(pdf_path), filename=os.path.basename(pdf_path), as_attachment=True)
    
    return render_template('index.html')

def create_pdf(image_paths, output_path):
    pdf = FPDF()
    for image_path in image_paths:
        cover = Image.open(image_path)
        width, height = cover.size
        pdf.add_page()
        pdf.image(image_path, 10, 10, 200)  # Modify to fit the image as needed
    pdf.output(output_path, "F")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
