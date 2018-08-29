"""Doc."""
import os
import json
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from processor import Processor


UPLOAD_FOLDER = '/tmp/uploads'

app = Flask(__name__)
api = Api(app)
pro = Processor()


if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def getpath(filename):
    return os.path.join(UPLOAD_FOLDER, filename)


@app.route('/')
def home():
    return send_from_directory('.', 'app.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['files[]']
    filename = secure_filename(file.filename)
    path = getpath(filename)
    file.save(path)
    pro.set_path(path)
    return json.dumps({'name': filename})


class Version(Resource):
    def get(self):
        return {'version': 0}


class Target(Resource):
    def get(self):
        return pro.get_target()

    def put(self):
        return pro.set_target(request.form)


class Job(Resource):
    def get(self):
        return pro.get_job()

    def put(self):
        return pro.set_job(request.form)


class Result(Resource):
    def get(self):
        return pro.get_result()


api.add_resource(Version, '/version')
api.add_resource(Target, '/target')
api.add_resource(Job, '/job')
api.add_resource(Result, '/result')


if __name__ == '__main__':
    app.run(debug=True)
