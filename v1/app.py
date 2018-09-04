"""Doc."""
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from processor import Processor
from storage import DocStore


app = Flask(__name__)
api = Api(app)
pro = Processor()
ds = DocStore()


@app.route('/')
def home():
    """Doc."""
    return send_from_directory('.', 'app.html')

@app.route('/favicon.ico')
def favicon():
    """Doc."""
    return send_from_directory('.', 'favicon.ico')


@app.route('/upload/<int:user_id>', methods=['POST'])
def upload_file(user_id):
    """Doc."""
    file = request.files['files[]']
    return pro.upload(user_id, file)


class Version(Resource):
    """Doc."""

    def get(self):
        """Doc."""
        return {'version': 0}


class UserId(Resource):
    """Doc."""

    def get(self, user_email):
        """Doc."""
        return {'user_id': 0}


class UserFile(Resource):
    """Doc."""

    def get(self, user_id):
        """Doc."""
        return pro.get_file(user_id)


class Target(Resource):
    """Doc."""

    def get(self, user_id):
        """Doc."""
        return pro.get_target(user_id)

    def put(self, user_id):
        """Doc."""
        return pro.set_target(user_id, request.form)


class Job(Resource):
    """Doc."""

    def get(self, user_id):
        """Doc."""
        return pro.get_job(user_id)

    def put(self, user_id):
        """Doc."""
        return pro.set_job(user_id, request.form)


class Result(Resource):
    """Doc."""

    def get(self, user_id):
        """Doc."""
        return pro.get_result(user_id)


api.add_resource(Version, '/version')
api.add_resource(UserId, '/user_id/<string:user_email>')
api.add_resource(UserFile, '/user_file/<int:user_id>')
api.add_resource(Target, '/target/<int:user_id>')
api.add_resource(Job, '/job/<int:user_id>')
api.add_resource(Result, '/result/<int:user_id>')


class MyTest(Resource):
    def get(self, user_id, job_id):
        return {'data': [user_id, job_id]}


api.add_resource(MyTest, '/mytest/<int:user_id>/<int:job_id>')


if __name__ == '__main__':
    app.run(debug=True)
