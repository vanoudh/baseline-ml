import os, json
from flask import Flask, request, send_from_directory, Response
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/uploads'

app = Flask(__name__)
api = Api(app)

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
    file.save(getpath(filename))
    return json.dumps({'name': filename})



class Version(Resource):
    def get(self):
        return {'version': 0}

api.add_resource(Version, '/version')

target = {
    'has_eaten': 'predictor',
    'is_hungry': 'target'
}

class Target(Resource):
    def get(self):
        return target
    def put(self):
        global target
        target = request.form
        print(type(target))
        print(target)
        return target

api.add_resource(Target, '/target')


job = None

class Job(Resource):
    def get(self):
        return job
    def put(self):
        global job
        job = request.form
        return job

api.add_resource(Job, '/job')


mock_result = {
    'columns': ['Model', 'Metric1', 'Metric2'],
    'r1': ['model-zero', 1, 1],
    'r2': ['auto-sklearn', 2, 3]
}

class Result(Resource):
    def get(self):
        return mock_result

api.add_resource(Result, '/result')




if __name__ == '__main__':
    app.run(debug=True)
