"""Doc."""
import os
import logging
import time
import json
from flask import Flask, request, send_from_directory, jsonify, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
import secrets
from subprocess import Popen
from werkzeug.utils import secure_filename

from email_checker import check_email
from user import User
from utils import read_csv
from storage_factory import ds, fs, put_result, get_result

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)


MODEL_LIST = 'zero linear tree forest'.split()


""" Utils """


def user_string(user):
    return "user {}: {}".format(user.id, user.is_authenticated)


def get_user_from_storage(user_id):
    js = ds.get('user', user_id)
    if js is None:
        return None
    user = User(user_id)
    user.password_hash = js['password_hash']
    user.auth = js['auth']
    return user


def save_user(user):
    logging.debug('save {}'.format(user_string(user)))
    js = {
        'password_hash': user.password_hash,
        'auth': user.auth
        }
    ds.put('user', user.id, js)


@login_manager.user_loader
def load_user(user_id):
    user = get_user_from_storage(user_id)
    logging.debug('loaded {}'.format(user_string(user)))
    return user


""" Definition of routes. """

import urllib3

@app.route('/')
def route_home():
    # url = 'https://raw.githubusercontent.com/vanoudh/hello/master/app.html'
    # return urllib3.PoolManager().request('GET', url).data
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def route_js():
    return send_from_directory('.', 'app.js')


@app.route('/favicon.ico')
def route_favicon():
    return send_from_directory('.', 'favicon.ico')


@app.route('/version')
def route_version():
    return jsonify({'version': 0})


@app.route('/login/<string:user_id>', methods=['POST'])
def route_login(user_id):
    user_id = request.form['email']
    password = request.form['password']
    user = get_user_from_storage(user_id)
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Login failed'})
    save_user(user)
    login_user(user)
    user_info = ds.get('user_info', user_id)
    first_name = user_info['first_name'] if user_info else user_id
    r = {
        'user_id': user_id, 
        'auth': user.is_authenticated, 
        'first_name': first_name
    }
    return jsonify(r)


@app.route('/register/<string:user_id>', methods=['POST'])
def route_register(user_id):
    user_id = request.form['email']
    password = request.form['password']
    logging.debug(user_id)
    user = get_user_from_storage(user_id)
    if user is not None:
        return jsonify({'message': 'User already registered'})
    if not check_email(user_id):
        return jsonify({'message': 'Invalid email'})
    user = User(user_id)
    user.set_password(password)
    user.check_password(password)
    save_user(user)
    login_user(user)
    user_info = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    ds.put('user_info', user_id, user_info)
    r = {
        'user_id': user_id, 
        'auth': user.is_authenticated, 
        'first_name': user_info['first_name']
    }
    return jsonify(r)


@app.route('/logout/<string:user_id>', methods=['POST'])
@login_required
def route_logout(user_id):
    logout_user()
    logout_option = request.form['logout_option']
    if logout_option == 'delete':
        logging.info('deleting account for {}'.format(user_id))
        filep = ds.get('file', user_id)
        if filep is not None:
            fs.delete(filep['filename']) 
        for kind in 'user target file result_zero result_linear result_tree result_forest score_desc'.split():
            ds.delete(kind, user_id)
    return jsonify({'logout': True, 'logout_option': logout_option})


@app.route('/user_file/<string:user_id>')
@login_required
def route_user_file(user_id):
    r = ds.get('file', user_id)
    return jsonify(r)


@app.route('/upload/<string:user_id>', methods=['POST'])
@login_required
def route_upload(user_id):
    print(request.files)
    file = request.files['files[]']
    source_filename = secure_filename(file.filename)
    filename = '-'.join(['data', user_id, source_filename])
    ds.put('file', user_id, {'filename': filename, 'source_filename': source_filename})
    fs.save(filename, file)
    path = fs.get_path(filename)
    vl = []
    message = "{}"
    try:
        df = read_csv(path)
        for c in df.columns:
            vl.append(c + 'p')
        ds.put('target', user_id, {'target':','.join(vl)})
    except Exception as e:
        logging.warning(e)
        message = "Failed to parse {}"            
        fs.delete(filename)
        ds.delete('file', user_id)
    return json.dumps({'name': message.format(source_filename)})


@app.route('/target/<string:user_id>', methods=['GET', 'PUT'])
@login_required
def route_target(user_id):
    if request.method == 'GET':
        r = ds.get('target', user_id)
    elif request.method == 'PUT':
        r = ds.put('target', user_id, request.form.to_dict())
    return jsonify(r)


def _run_job(user_id, model):
    logging.info('run {}'.format(model))
    cmd = "python automl_run.py {} {}".format(user_id, model)
    # fname_out = "{}/run-{}-{}.log".format(LOG_FOLDER, user_id, model)
    # with open(fname_out, "wb") as out:
    job = Popen(cmd, shell=True)
    logging.debug('rcode {}'.format(job.returncode))


@app.route('/job/<string:user_id>', methods=['POST'])
@login_required
def route_job(user_id):

    for m in MODEL_LIST:
        put_result(m, user_id, 'running', 'pending...')

    _run_job(user_id, 'all')
    return route_result(user_id)


@app.route('/result/<string:user_id>', methods=['GET'])
@login_required
def route_result(user_id):
    r = list(map(lambda m:get_result(m, user_id) , MODEL_LIST))
    j = {}
    for m, rr in zip(MODEL_LIST, r):
        j[m] = rr
    sd = ds.get('score_desc', user_id)
    j['score_desc'] = sd['score_desc'] if sd else 'Result'
    return jsonify(j)
