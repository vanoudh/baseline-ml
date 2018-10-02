"""Doc."""
import os
import logging
import time
from flask import Flask, request, send_from_directory, jsonify, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
import secrets

from app_processor import Processor
from email_checker import check_email
from user import User
from storage_factory import fs, ds

logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)
processor = Processor()


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

@app.route('/')
def route_home():
    # if request.url.startswith('http://baseline-ml.appspot.com'):
    #     url = request.url.replace('http', 'https', 1)
    #     return redirect(url, code=302)
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
    return jsonify(processor.get_file(user_id))


@app.route('/upload/<string:user_id>', methods=['POST'])
@login_required
def route_upload(user_id):
    file = request.files['files[]']
    return processor.upload(user_id, file)


@app.route('/target/<string:user_id>', methods=['GET', 'PUT'])
@login_required
def route_target(user_id):
    if request.method == 'GET':
        r = processor.get_target(user_id)
    elif request.method == 'PUT':
        r = processor.set_target(user_id, request.form.to_dict())
    return jsonify(r)


@app.route('/job/<string:user_id>', methods=['POST'])
@login_required
def route_job(user_id):
    print(request.form)
    r = processor.run_job(user_id, request.form.to_dict())
    return jsonify(r)


@app.route('/result/<string:user_id>', methods=['GET'])
@login_required
def route_result(user_id):
    r = processor.get_result(user_id)
    return jsonify(r)
