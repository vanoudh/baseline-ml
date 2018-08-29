"""Doc."""
import json
import pandas as pd
from subprocess import Popen

class Processor:
    """Doc."""

    def __init__(self):
        """Doc."""
        self.path = None
        self.target = None
        self.job = None
        self.result = None

    def set_path(self, path):
        """Doc."""
        self.path = path

    def set_target(self, t):
        """Doc."""
        self.target = t
        return self.target

    def get_target(self):
        """Doc."""
        if self.path is None:
            return {'error': 'no file has been set'}
        if self.target is None:
            self.target = {}
            df = pd.read_csv(self.path)
            for c in df.columns:
                self.target[c] = 'predictor'
        return self.target

    def set_job(self, job):
        """Doc."""
        if 'control' not in job:
            return {'error': 'missing control command'}
        control = job['control']
        if control not in 'start stop'.split():
            return {'error': 'unexpected control value'}
        if control == 'start':
            self.job = Popen([". ./runjob.sh"], shell=True)
        elif control == 'stop':
            if self.job is None:
                return {'error': 'stop on non existing job'}
            print('terminate job')
            self.job.terminate()
        return self.get_job()

    def get_job(self):
        """Doc."""
        if self.job is None:
            return {'error': 'no job'}
        self.job.poll()
        return {'pid': self.job.pid, 'returncode': self.job.returncode}

    def get_result(self):
        """Doc."""
        with open('result.json') as f:
            return json.load(f)
