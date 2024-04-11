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
from flask import send_from_directory
# other imports
from fpdf import FPDF

def create_pdf(image_paths, output_path):
    pdf = FPDF()
    for image_path in image_paths:
        try:
            cover = Image.open(image_path)
            width, height = cover.size
            pdf.add_page()
            # Assuming images are not larger than A4 size, adjust as needed
            pdf.image(image_path, 10, 10, 200)  # Sizes can be adjusted based on your need
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
    pdf.output(output_path, "F")

@app.route('/download-pdf')
def download_pdf():
    pdf_filename = 'document.pdf'
    directory = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory, pdf_filename, as_attachment=True)

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
        pdf_filename = 'document.pdf'
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        create_pdf(image_paths, pdf_path)
        return redirect(url_for('download_pdf'))  # Redirect to download handler
    
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
