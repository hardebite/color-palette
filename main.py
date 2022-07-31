import time

from resizeimage import resizeimage
from PIL import Image
import webcolors
from colorthief import ColorThief
from flask import Flask, render_template ,redirect,url_for,request, flash,send_from_directory
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import os
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
form=[]
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form=[]
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('colors', name=filename))
    return render_template("index.html", form=form)
@app.route('/uploads/<name>')
def download_file(name):
    print(name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
@app.route("/colors",methods=["POST","GET"])
def colors():

    image_path = f'static/{filename}'
    new_image_path = './data.jpg'

    with open(image_path, 'r+b') as f:
        with Image.open(f) as image:

            # Resize
            if image.width<800:
                # print("yes")
                # larger_image = resizeimage.resize("width", image, 800)
                # print("done")
                flash("image is too small")
                return render_template("index.html",message= "Error: The image width is too small !!!")


            smaller_image = resizeimage.resize_width(image, 800)
            smaller_image.save(new_image_path, image.format)

            # Get Colors
            color_thief = ColorThief(new_image_path)
            color_palette = color_thief.get_palette(color_count=10, quality=10)
            for color in color_palette:
                form.append(webcolors.rgb_to_hex(color))
                print(form)
            name = filename
            print(name)

    return render_template("color.html",form=form,name=filename)

if __name__=="__main__":
    app.run(debug=True)