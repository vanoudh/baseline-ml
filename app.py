"""Doc."""
from flask import Flask, request, send_from_directory, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from processor import Processor
from storage import DocStore
from email_checker import check_email
from user import User


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

pro = Processor()
ds = DocStore()


def user_string(user):
    """Doc."""
    return "user {}: {}".format(user.id, user.is_authenticated)


def get_user_from_storage(user_id):
    """Doc."""
    js = ds.get(user_id, 'user')
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
        'id': user.id,
        'password_hash': user.password_hash,
        'auth': user.auth
        }
    ds.put(user.id, 'user', js, overwrite=True)


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
    print(user_id, password)
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


# @app.route('/user_id/<string:user_email>')
# @login_required
# def _user_id():
#     """Doc."""
#     return jsonify({'user_id': 0})


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
        r = pro.set_target(user_id, request.form)
    return jsonify(r)


@app.route('/job/<string:user_id>', methods=['GET', 'PUT'])
@login_required
def _job(user_id):
    """Doc."""
    if request.method == 'GET':
        r = pro.get_job(user_id)
    elif request.method == 'PUT':
        r = pro.set_job(user_id, request.form)
    return jsonify(r)


@app.route('/result/<string:user_id>')
@login_required
def _result(user_id):
    """Doc."""
    r = pro.get_result(user_id)
    return jsonify(r)


if __name__ == '__main__':
    app.secret_key = '42'
    app.config['JSON_SORT_KEYS'] = False
    app.run(debug=True)
    # app.run(ssl_context='adhoc')
