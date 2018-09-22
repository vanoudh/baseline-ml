
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from Mlb import Mlb

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getpath(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(getpath(filename))
            return redirect(url_for('validate', filename=filename))
    return render_template('upload.html')


@app.route('/validate/<filename>')
def validate(filename):
    path = getpath(filename)
    mlb = Mlb()
    columns = mlb.prerun(path)
    return render_template('validate.html', filename=filename, columns=columns)

@app.route('/run/<filename>')
def run(filename):
    logging.info('---')
    logging.info(request.args)
    x_cols = [k[5:] for k in request.args if k.startswith('pred_')]
    y_cols = [k[5:] for k in request.args if k.startswith('targ_')]
    path = getpath(filename)
    mlb = Mlb()
    result = mlb.run(path, x_cols, y_cols)
    return render_template('result.html', result=result)
