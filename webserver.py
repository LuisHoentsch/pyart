import io
from flask import Flask, render_template, request, send_file
import re

from image_manipulation import alter_image

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    colora = request.form.get('string1').lower()
    colorb = request.form.get('string2').lower()
    # Check if colors properly specified
    if re.match(r'^#?([0-9a-f]{6})$', colora) is None or re.match(r'^#?([0-9a-f]{6})$', colorb) is None:
        return "Provide color in hex format (e.g. #aa12ff).", 400
    # Check if file is empty
    if not file:
        return "No file provided.", 400
    # Check file size
    if len(file.read()) > 20 * 1024 * 1024:  # Max file size: 20MB
        return "File is too large. Max file size 20MB.", 400
    file.seek(0)  # Reset file pointer to beginning
    image = alter_image(file, colora, colorb)
    return send_file(io.BytesIO(image), as_attachment=True, mimetype="image/png", download_name="converted.png")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
