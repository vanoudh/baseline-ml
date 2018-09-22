"""Doc."""
import os
import time
import json
import logging
from subprocess import Popen
from werkzeug.utils import secure_filename

from utils import read_csv
from storage_factory import ds, fs

LOG_FOLDER = '.logs'

if not os.path.isdir(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

MODEL_LIST = 'no-model linear-model forest-model auto-sklearn'.split()


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
        source_filename = secure_filename(file.filename)
        filename = '-'.join(['data', user_id, source_filename])
        ds.put('file', user_id, {'filename': filename, 'source_filename': source_filename})
        fs.save(filename, file)
        path = fs.get_path(filename)
        target = {}
        message = "{}"
        try:
            df = read_csv(path)
            for c in df.columns:
                target[c] = 'predictor'
            self.set_target(user_id, target)
        except Exception as e:
            logging.warning(e)
            message = "error while parsing {}"            
        return json.dumps({'name': message.format(source_filename)})

    def get_target(self, user_id):
        """Doc."""
        r = ds.get('target', user_id)
        return r

    def set_target(self, user_id, t):
        """Doc."""
        ds.put('target', user_id, t)
        return t

    def _run_job(self, user_id, model):
        logging.info('run {}'.format(model))
        ds.put('result-{}'.format(model), user_id, {'result': 'starting...'})
        cmd = "python automl_run.py {} {}".format(user_id, model)
        fname_out = "{}/run-{}-{}.log".format(LOG_FOLDER, user_id, model)
        with open(fname_out, "wb") as out:
            job = Popen(cmd, shell=True, stdout=out)
        logging.debug('rcode {}'.format(job.returncode))
    
    def run_job(self, user_id, job):
        """Doc."""
        for m in MODEL_LIST:
            self._run_job(user_id, m)
        return self.get_result(user_id)
        
    def get_result(self, user_id):
        """Doc."""

        def getr(m):
            r = ds.get('result-{}'.format(m), user_id)
            if r is None:
                return '----'
            return r['result']

        r = list(map(getr , MODEL_LIST))
        j = {}
        for m, rr in zip(MODEL_LIST, r):
            j[m] = rr
        j['done'] = ('starting...' not in r) and ('learning...' not in r)  
        return j
