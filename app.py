from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os, json
from datetime import datetime

from datetime import datetime
import pytz
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DATA_FILE = 'photos.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load photos
def load_photos():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save photos
def save_photos(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    photos = load_photos()
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload():
    title = request.form.get('title')
    photo = request.files.get('photo')

    if not photo or photo.filename == '':
        return redirect('/')

    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))

    photos = load_photos()

    # Set timezone to Philippine Time
    ph_tz = pytz.timezone("Asia/Manila")
    now = datetime.now(ph_tz)

    photos.append({
        "title": title,
        "filename": photo.filename,
        "date": now.strftime("%B %d, %Y • %I:%M %p")  # e.g., Feb 20, 2026 • 07:13 PM
    })
    save_photos(photos)

        
        
    return redirect('/')

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    photos = load_photos()
    photos = [p for p in photos if p['filename'] != filename]
    save_photos(photos)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect('/')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)