from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config ['UPLOAD_FOLDER'] = 'uploader/'


allowed_extensions = set(['jpg','jpeg','png'])

@app.route('/')
def main():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.route('/gallery.html')
def gallery():
    return render_template('gallery.html')

@app.route('/product-page.html')
def product():
    return render_template('product-page.html')

@app.route('/features.html')
def features():
    return render_template('features.html')


def allowed_file(filename):
  return '.' in filename and \
       filename.rsplit('.', 1)[1] in allowed_extensions

@app.route("/input-text", methods=["POST"])
def insert_text():
    text = request.form['base']
    value = 20
    try:
        value = int(text)
    except ValueError:
        print("Invalid integer")
    return render_template('product-page.html'), str(value)

@app.route("/upload-image", methods=["GET","POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            input_image = request.files['image']


            if input_image.filename=="":
                print("Image must have filename")
                return redirect(request.url)

            if allowed_file(input_image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                print("Image saved")
                filename = secure_filename(input_image.filename)
                input_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('product-page.html')

if __name__ == '__main__':
    app.run(debug=True)
