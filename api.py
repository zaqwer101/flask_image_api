from flask import Flask, flash, jsonify, request, make_response

def check_file(file):
    if not file.filename.split('.')[-1] in ['jpg', 'png']:
        return False
    return True

app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    """Обработка загрузки изображений"""
    if 'file' not in request.files:
        return make_response(jsonify({"error": "no file provided"}), 400)
    file = request.files['file']
    if not check_file(file):
        return make_response(jsonify({"error": "JPG or PNG file expected"}), 400)
    app.logger.debug(f"Filename: {file.filename}")
    return make_response(jsonify({"message": "success"}), 200)