from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
script_dir = os.path.dirname(os.path.abspath(__file__))
upload_path = lib_path = os.path.join(script_dir, 'pic')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_path  # Set path to your image folder
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Get the list of images in the upload folder
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [img for img in images if allowed_file(img)]  # Filter only allowed image types
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully', 200
    return 'Invalid file type', 400

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
