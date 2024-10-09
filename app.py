from flask import Flask, request, render_template, url_for, jsonify
from PIL import Image
from ultralytics import YOLO
import os

app = Flask(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
static_directory = os.path.join(current_directory, 'static')
UPLOAD_FOLDER = os.path.join(static_directory, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('index.html', image_path=None, prediction=None)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    prediction = predict(file_path)

    image_url = url_for('static', filename=f'uploads/{file.filename}', _external=True)
    return jsonify({'image_path': image_url, 'prediction': prediction})

def predict(image_path):
    with Image.open(image_path) as img:
        model_path = os.path.join(app.static_folder, 'runs/detect/train/weights/best.pt')
        model = YOLO(model_path)
        results = model(img)

        mineral = "Probabily does not contain any of the 4 mentioned minerals"
        if results and results[0].boxes:
            index = int(results[0].boxes[0].cls.item())
            if index == 0:
                mineral = "Biotite"
            elif index == 2:
                mineral = "Chrysocolla"
            elif index == 4:
                mineral = "Pyrite"
            elif index == 5:
                mineral = "Quartz"
        
        return f'{mineral}'

if __name__ == '__main__':
    app.run(debug=True)
