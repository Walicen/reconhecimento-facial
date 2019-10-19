from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os

from face_detection import detectar_faces

SECRET_KEY = "F!Z<6M]gqhuClx[1W)eVZ?^Ng{[+a2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ASSETS
app.secret_key = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Chama detecção de face
            image_name = detectar_faces(filename)
            if image_name:
                return redirect(url_for('uploaded_file', filename=image_name))
            else:
                flash("Nenhuma Face detectada")

    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
