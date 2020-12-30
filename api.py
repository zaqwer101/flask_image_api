from flask import Flask, flash, jsonify, request, make_response, render_template, redirect, url_for
from PIL import Image
import os
import datetime

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']
UPLOAD_FOLDER = 'static/images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'asdfjuihgu8ihvb9823u489qhjadu89fghdyufgvbyw78y7'

def check_file(file):
    return file.filename.split('.')[-1] in ALLOWED_EXTENSIONS


@app.after_request
def add_header(r):
    """
    Отключаем кеширование
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# И ещё раз отключаем кеширование
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def process_image(path):
    """ Обработать изображение """
    
    filename = path.split('/')[-1]
    location = UPLOAD_FOLDER + "/" + filename
    
    image = Image.open(path)
    new_image = image.resize((512,512))
    new_image = new_image.convert('L')
    new_image.save(location)
    os.remove(path)


@app.route('/', methods=['POST'])
def upload_post():
    """ Обработка загрузки изображений через прямой POST-запрос """
    if 'file' not in request.files:
        return make_response(jsonify({"error": "no file provided"}), 400)
    file = request.files['file']
    if not check_file(file):
        return make_response(jsonify({"error": "JPG or PNG file expected"}), 400)

    image_filename = f"{app.config['UPLOAD_FOLDER']}/{file.filename}"

    file.save(image_filename)
    image = Image.open(image_filename)
    image_size = image.size
    image_upload_date = datetime.datetime.now()
    return make_response(jsonify({'size': image_size, 'name': file.filename, 'upload_date': image_upload_date}), 200)


@app.route('/webupload', methods=['POST'])
def upload_web():
    """ Обработка загрузки изображений через POST-запрос с web-формы """
    if 'file' not in request.files:
        flash('No file provided')
        return redirect(url_for('render_upload_form'))
    file = request.files['file']
    
    if file.filename == '':
        flash('No image selected')
        return redirect(url_for('render_upload_form'))
    
    if check_file(file):
        flash("Изображение загружено")

        # сохраняем исходный файл
        tmp_file_location = f"{app.config['UPLOAD_FOLDER']}/tmp/{file.filename}"
        file.save(tmp_file_location)

        # обрабатываем файл и сохраняем его новую версию
        process_image(tmp_file_location)

        return redirect(url_for('render_upload_form', image=file.filename))
    else:
        flash(f'Разрешены только расширения {ALLOWED_EXTENSIONS}')
        return redirect(url_for('render_upload_form'))


@app.route('/', methods=['GET'])
def render_upload_form():
    """ Форма загрузки изображения """
    if 'image' in request.args:
        return render_template('index.html', filename=request.args['image'])
    else:
        return render_template('index.html')


@app.route('/images/<image>')
def display_image(image):
    return redirect(url_for('static', filename=f'images/{image}'), code=301)

