"""Doc."""
import os
import time
import json
import logging
from subprocess import Popen
from werkzeug.utils import secure_filename

from utils import read_csv
from storage_factory import ds, fs, put_result, get_result


MODEL_LIST = 'zero linear tree forest'.split()


class Processor:

    def __init__(self):
        pass

    def get_file(self, user_id):
        try:
            return ds.get('file', user_id)
        except FileNotFoundError:
            return {'filename': "No file yest, please upload one"}

    def upload(self, user_id, file):
        source_filename = secure_filename(file.filename)
        filename = '-'.join(['data', user_id, source_filename])
        ds.put('file', user_id, {'filename': filename, 'source_filename': source_filename})
        fs.save(filename, file)
        path = fs.get_path(filename)
        vl = []
        message = "{}"
        try:
            df = read_csv(path)
            for c in df.columns:
                vl.append(c + 'p')
            self.set_target(user_id, {'target':','.join(vl)})
        except Exception as e:
            logging.warning(e)
            message = "Failed to parse {}"            
            fs.delete(filename)
            ds.delete('file', user_id)
        return json.dumps({'name': message.format(source_filename)})

    def get_target(self, user_id):
        r = ds.get('target', user_id)
        return r

    def set_target(self, user_id, t):
        ds.put('target', user_id, t)
        return None

    def _run_job(self, user_id, model):
        logging.info('run {}'.format(model))
        put_result(model, user_id, 'running', 'starting...')
        cmd = "python automl_run.py {} {}".format(user_id, model)
        # fname_out = "{}/run-{}-{}.log".format(LOG_FOLDER, user_id, model)
        # with open(fname_out, "wb") as out:
        job = Popen(cmd, shell=True)
        logging.debug('rcode {}'.format(job.returncode))
    
    def run_job(self, user_id, job):
        for m in MODEL_LIST:
            self._run_job(user_id, m)
        return self.get_result(user_id)
        
    def get_result(self, user_id):

        def getr(m):
            return get_result(m, user_id)

        r = list(map(getr , MODEL_LIST))
        j = {}
        for m, rr in zip(MODEL_LIST, r):
            j[m] = rr
        
        sd = ds.get('score_desc', user_id)
        j['score_desc'] = sd['score_desc'] if sd else 'Result'
        return j
