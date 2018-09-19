"""Doc."""
import os
import time
import json
import pandas as pd
from subprocess import Popen
from werkzeug.utils import secure_filename

from storage_factory import ds, fs


MODEL_LIST = 'no-model linear-model auto-sklearn'.split()


class Processor:
    """Doc."""

    def __init__(self):
        """Doc."""
        pass

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

    def run_job(self, user_id, model):
        print('run {}'.format(model))
        res = {'result': 'running...'}
        ds.put('result-{}'.format(model), user_id, res)
        cmd = "python automl_run.py {} {}".format(user_id, model)
        job = Popen(cmd, shell=True)
        time.sleep(1)
        job.poll()
        if job.returncode is not None:
            if job.returncode >= 1:
                res = {'result': 'job failed'}
                ds.put('result-{}'.format(model), user_id, res)
        print('rcode {}'.format(job.returncode))
    
    def set_job(self, user_id, job):
        """Doc."""
        for m in MODEL_LIST:
            self.run_job(user_id, m)
        return self.get_job(user_id)

    def get_job(self, user_id):
        """Doc."""
        f = lambda m:ds.get('result-{}'.format(m), user_id)['result']
        r = list(map(f , MODEL_LIST))
        done = 'running...' not in r
        return { 
            MODEL_LIST[0]: r[0],
            MODEL_LIST[1]: r[1],
            MODEL_LIST[2]: r[2],
            'done': done
            }

    def get_result(self, user_id):
        """Doc."""
        return ds.get('result', user_id)
