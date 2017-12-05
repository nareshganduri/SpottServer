import os
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath('./static/img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_date(filename):
    import time
    date_string = filename[5:20]
    t = time.strptime(date_string, '%Y%m%d_%H%M%S')
    clk = str(t.tm_hour % 12) + ':' + '%02d' % t.tm_min
    clk += ' AM' if t.tm_hour < 12 else ' PM'
    return clk

def get_location(filename):
    import piexif

    # get location from metadata
    exif_dict = piexif.load(filename)
    return int(exif_dict['Exif'][piexif.ExifIFD.UserComment])

@app.route('/')
def list_images():
    imgs_dir = 'static/img'
    img_files = [f for f in os.listdir(imgs_dir) if os.path.isfile(os.path.join(imgs_dir, f))]
    images = []
    for f in img_files:
        image = {}
        image['title'] = f
        image['src'] = '/static/img/' + f
        image['date'] = get_date(f)

        full_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
        image['location'] = ['Left', 'Center', 'Right'][get_location(full_path)] + ' Side'
        images.append(image)
    return render_template('index.html',
                           images=images)

@app.route('/upload_test')
def test_img_upload():
    return render_template('upload_test.html')

@app.route('/download_test')
def test_img_download():
    return render_template('download_test.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        img_data = request.files['src']
        filename = request.form['date']
        location = request.form['location']

        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img_data.save(full_path)

        # resize the image to fit
        from PIL import Image
        import piexif

        basewidth = 480
        img = Image.open(full_path)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(full_path)

        # update metadata to store location
        piexif.remove(full_path)
        exif_dict = piexif.load(full_path)
        exif_dict['Exif'] = {piexif.ExifIFD.UserComment:str(location)}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, full_path)

        return 'SUCCESS'

@app.route('/download', methods=['POST'])
def download_image():
    if request.method == 'POST':
        req_location = request.form['location']

        imgs_dir = 'static/img'
        img_files = [f for f in os.listdir(imgs_dir) if os.path.isfile(os.path.join(imgs_dir, f))]
        images = []
        for f in img_files:
            image = {}
            image['date'] = get_date(f)

            full_path = os.path.join(app.config['UPLOAD_FOLDER'], f)
            with open(full_path, 'rb') as img_data:
                raw_bytes = img_data.read()
                image['data'] = raw_bytes.encode('base64')
            location = str(get_location(full_path))

            if location == req_location or req_location == "3":
                images.append(image)

        from flask import jsonify
        return jsonify(images)
