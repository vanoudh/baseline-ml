"""Doc."""
import os
from flask import Flask, request, send_from_directory, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
import secrets

from processor import Processor
from email_checker import check_email
from user import User
from storage_factory import ds


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['JSON_SORT_KEYS'] = False
login_manager = LoginManager()
login_manager.init_app(app)

pro = Processor()


def user_string(user):
    """Doc."""
    return "user {}: {}".format(user.id, user.is_authenticated)


def get_user_from_storage(user_id):
    """Doc."""
    js = ds.get('user', user_id)
    if js is None:
        return None
    user = User(user_id)
    user.password_hash = js['password_hash']
    user.auth = js['auth']
    return user


def save_user(user):
    """Doc."""
    print('save {}'.format(user_string(user)))
    js = {
        'password_hash': user.password_hash,
        'auth': user.auth
        }
    ds.put('user', user.id, js)


@login_manager.user_loader
def load_user(user_id):
    """Doc."""
    user = get_user_from_storage(user_id)
    print('loaded {}'.format(user_string(user)))
    return user


""" Definition of routes. """


@app.route('/')
def _home():
    """Doc."""
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def _js():
    """Doc."""
    return send_from_directory('.', 'app.js')


@app.route('/favicon.ico')
def _favicon():
    """Doc."""
    return send_from_directory('.', 'favicon.ico')


@app.route('/version')
def _version():
    """Doc."""
    return jsonify({'version': 0})


@app.route('/upload/<string:user_id>', methods=['POST'])
@login_required
def _upload(user_id):
    """Doc."""
    file = request.files['files[]']
    return pro.upload(user_id, file)


@app.route('/register', methods=['POST'])
def _register():
    """Doc."""
    user_id = request.form['email']
    password = request.form['password']
    print(user_id)
    user = get_user_from_storage(user_id)
    if user is not None:
        return jsonify({'message': 'user already registered'})
    if not check_email(user_id):
        return jsonify({'message': 'invalid email'})
    user = User(user_id)
    user.set_password(password)
    user.check_password(password)
    save_user(user)
    login_user(user)
    return jsonify({'user_id': user_id, 'auth': user.is_authenticated})


@app.route('/login', methods=['POST'])
def _login():
    """Doc."""
    user_id = request.form['email']
    password = request.form['password']
    print(user_id)
    user = get_user_from_storage(user_id)
    if user is None or not user.check_password(password):
        return jsonify({'message': 'login failed'})
    save_user(user)
    login_user(user)
    return jsonify({'user_id': user_id, 'auth': user.is_authenticated})


@app.route('/logout', methods=['POST'])
@login_required
def _logout():
    """Doc."""
    logout_user()
    return jsonify({'logout': True})


# @app.route('/feedback/<string:user_id>', methods=['POST'])
# def _feedback(user_id):
#     """Doc."""
#     data = request.form.to_dict()
#     if list(data.keys())[0] != 'text':
#         return jsonify({'message': 'unexpected content'})
#     data['text'] = data['text'][:6000] 
#     ds.put('feedback', user_id, data)
#     return jsonify({'user_id': user_id})


@app.route('/user_file/<string:user_id>')
@login_required
def _user_file(user_id):
    """Doc."""
    return jsonify(pro.get_file(user_id))


@app.route('/target/<string:user_id>', methods=['GET', 'PUT'])
@login_required
def _target(user_id):
    """Doc."""
    if request.method == 'GET':
        r = pro.get_target(user_id)
    elif request.method == 'PUT':
        r = pro.set_target(user_id, request.form.to_dict())
    return jsonify(r)


@app.route('/job/<string:user_id>', methods=['GET', 'PUT'])
@login_required
def _job(user_id):
    """Doc."""
    if request.method == 'GET':
        r = pro.get_job(user_id)
    elif request.method == 'PUT':
        r = pro.set_job(user_id, request.form.to_dict())
    return jsonify(r)


@app.route('/result/<string:user_id>')
@login_required
def _result(user_id):
    """Doc."""
    r = pro.get_result(user_id)
    return jsonify(r)


# if __name__ == '__main__':
#     app.run(debug=False)
#     # app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=443)
