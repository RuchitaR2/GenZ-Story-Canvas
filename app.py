from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Store stories and images
posts = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story_canvas', methods=['GET', 'POST'])
def story_canvas():
    if request.method == 'POST':
        if 'image' not in request.files or 'caption' not in request.form:
            return redirect(request.url)
        
        image = request.files['image']
        caption = request.form['caption']
        
        if image and allowed_file(image.filename):
            filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            posts.append({'image': filename, 'caption': caption})
        
        return redirect(url_for('story_canvas'))
    
    return render_template('story_canvas.html', posts=posts)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
