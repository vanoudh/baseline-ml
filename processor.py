"""Doc."""
import json
import pandas as pd
from subprocess import Popen
from werkzeug.utils import secure_filename
from storage import FileStore, DocStore


fs = FileStore()
ds = DocStore()


class Processor:
    """Doc."""

    def __init__(self):
        """Doc."""
        self.is_mock = True
        self.job = None

    def get_file(self, user_id):
        """Doc."""
        try:
            return ds.get(user_id, 'file')
        except FileNotFoundError:
            return "no file, please upload one"

    def upload(self, user_id, file):
        """Doc."""
        filename = secure_filename(file.filename)
        ds.put(user_id, 'file', filename, overwrite=True)
        self.is_mock = filename.find('mock') >= 0
        fs.save(user_id, 'dataset', file)
        target = {}
        df = pd.read_csv(fs.get_path(user_id, 'dataset'))
        for c in df.columns:
            target[c] = 'predictor'
        self.set_target(user_id, target)
        return json.dumps({'name': filename})

    def get_target(self, user_id):
        """Doc."""
        return ds.get(user_id, 'target')

    def set_target(self, user_id, t):
        """Doc."""
        ds.put(user_id, 'target', t, overwrite=True)
        return t

    def set_job(self, user_id, job):
        """Doc."""
        if 'control' not in job:
            return {'error': 'missing control command'}
        control = job['control']
        if control not in 'start stop'.split():
            return {'error': 'unexpected control value'}
        if control == 'start':
            model = "mock" if self.is_mock else "auto-sklearn"
            cmd = "python autosk.py {} {}".format(user_id, model)
            self.job = Popen(cmd, shell=True)
        elif control == 'stop':
            if self.job is None:
                return {'error': 'stop on non existing job'}
            print('terminate job')
            self.job.terminate()
        return self.get_job(user_id)

    def get_job(self, user_id):
        """Doc."""
        if self.job is None:
            return {'error': 'no job'}
        self.job.poll()
        return {'pid': self.job.pid, 'returncode': self.job.returncode}

    def get_result(self, user_id):
        """Doc."""
        return ds.get(user_id, 'result')
