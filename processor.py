"""Doc."""
import os
import json
import pandas as pd
from subprocess import Popen
from werkzeug.utils import secure_filename

from storage_factory import ds, fs


class Processor:
    """Doc."""

    def __init__(self):
        """Doc."""
        self.job = None

    def get_file(self, user_id):
        """Doc."""
        try:
            return ds.get('file', user_id)
        except FileNotFoundError:
            return {'filename': "no file, please upload one"}

    def upload(self, user_id, file):
        """Doc."""
        filename = secure_filename(file.filename)
        ds.put('file', user_id, {'filename': filename})
        self.is_mock = filename.find('mock') >= 0
        fs.save('dataset', user_id, file)
        target = {}
        path = fs.get_path('dataset', user_id)
        df = pd.read_csv(path)
        for c in df.columns:
            target[c] = 'predictor'
        self.set_target(user_id, target)
        return json.dumps({'name': filename})

    def get_target(self, user_id):
        """Doc."""
        return ds.get('target', user_id)

    def set_target(self, user_id, t):
        """Doc."""
        ds.put('target', user_id, t)
        return t

    def set_job(self, user_id, job):
        """Doc."""
        if 'control' not in job:
            return {'error': 'missing control command'}
        control = job['control']
        if control not in 'start stop'.split():
            return {'error': 'unexpected control value'}
        if control == 'start':
            model = "auto-sklearn"
            cmd = "python automl_run.py {} {}".format(user_id, model)
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
        return ds.get('result', user_id)
