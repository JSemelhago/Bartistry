from flask import Flask, request, render_template, redirect, send_file
from werkzeug.utils import secure_filename
import cv2
import glob
import numpy as np
from PIL import Image
import pandas as pd
import os

value=20

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
    try:
        value = int(text)
    except ValueError:
        print("Invalid integer")
    return render_template('product-page.html')

@app.route("/python", methods=["GET", "POST"])
def bartistry():
    # Find image
    img_path = [glob.glob('uploader/' + e) for e in ['*.jpg', '*.jpeg', '*.png']][0][0]

    if img_path:
        print('Image successfully found!')

    # Load image
    img = cv2.imread(img_path)

    if img.any():
        print('Image successfully read!')

    # Create mask and models for foreground and background
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Convert to and apply gray scale
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.bitwise_not(gray_scale)

    # Get contours from gray scale
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Get rectangle coordinates from around contours
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    contour = contours[max_index]

    x, y, w, h = cv2.boundingRect(contour)

    # If rectangle isn't properly drawn, use up to total size of image
    if x == 0:
        x += img.shape[1] - 1
    if y == 0:
        y += img.shape[0] - 1
    rect = (x, y, x + w, y + h)

    # Grab foreground from rectangle
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    cut_mask = np.where((mask == 2) | (mask == 0), 255, 1).astype('uint8')

    if cut_mask.any():
        print('Image mask successfully created!')

    img = img * cut_mask[:, :, np.newaxis]

    if img.any():
        print('Image successfully processed!')

    # Output image
    cv2.imwrite('../output/black_bkg.jpg', img)

    # Find jpg and open it using Pillow
    img_path = glob.glob('../output/*.jpg')[0]
    img = Image.open(img_path)

    if img:
        print('Pillow successfully read image!')

    # Get proportionally sized down image
    percent = (value / float(img.size[0]))
    height = int((float(img.size[1]) * float(percent)))

    result = img.resize((value, height), Image.ANTIALIAS)

    if result:
        print('Image successfully pixellated!')

    # Convert to dataframe with arrays representing colours
    pixel_array = np.array(result)
    df = pd.DataFrame(pixel_array.tolist())

    b = '🅱️'
    space = len(b)

    final_output = ''

    for index, row in df.iterrows():
        for entry in row:
            if int(entry[0]) > 5 or int(entry[1]) > 5 or int(entry[2]) > 5:
                final_output += b
            else:
                final_output += space * ' '
        final_output += '\n'

    if final_output:
        print('Text successfully created!')

    with open('../output/bartist.txt', 'w+', encoding='utf-8') as file:
        file.write(final_output)
        file.close()

    if os.path.isfile('../output/bartist.txt'):
        print('Text file successfully created!')

    return render_template('product-page.html')

@app.route("/upload-image", methods=["GET","POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            input_image = request.files['image']


            if input_image.filename=="":
                print("Image must have filename")
                return redirect(request.url)

            print("Image saved")
            filename = secure_filename(input_image.filename)
            input_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('product-page.html')

if __name__ == '__main__':
    app.run(debug=True)
