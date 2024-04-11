from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Max Upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def process_image(file_path):
    image = cv2.imread(file_path)
    if image is None:
        return None  # Check if image read successfully

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            docCnt = approx
            warped = four_point_transform(gray, docCnt.reshape(4, 2))
            return warped
    return None  # Return None if no appropriate contour was found

def four_point_transform(image, pts):
    # Implementation of four point transform
    pass  # Assuming you have this implemented correctly

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    ensure_upload_folder()  # Ensure the upload folder exists at every request
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            processed_image = process_image(file_path)
            if processed_image is None:
                return "Document could not be processed, please ensure it is a clear image of a document."
            result_path = file_path.replace('.jpg', '_processed.jpg').replace('.png', '_processed.png').replace('.jpeg', '_processed.jpeg')
            cv2.imwrite(result_path, processed_image)
            return send_from_directory(directory=os.path.dirname(result_path), filename=os.path.basename(result_path), as_attachment=True)
        return "Invalid file or no file uploaded."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
