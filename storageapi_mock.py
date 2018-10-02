"""Doc."""
import os
import json

STORAGE_FOLDER = '.store_mock'
S = '-'

if not os.path.isdir(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)


class FileStore:
    """Doc."""

    def save(self, filename, file):
        """Doc."""
        path = self.get_path(filename)
        file.save(path)

    def get_path(self, filename):
        """Doc."""
        return os.path.join(STORAGE_FOLDER, filename)

    def delete(self, filename):
        """Doc."""
        path = self.get_path(filename)
        try:
            os.remove(path)
        except OSError:
            pass


class DocStore:
    """Doc."""

    def _get_path(self, kind, name):
        """Doc."""
        li = [str(kind), str(name), 'json']
        return os.path.join(STORAGE_FOLDER, S.join(li))

    def put(self, kind, name, doc):
        """Doc."""
        path = self._get_path(kind, name)
        with open(path, 'w') as f:
            json.dump(doc, f)

    def log(self, kind, doc):
        """Doc."""
        path = self._get_path(kind, 'log')
        with open(path, 'a') as f:
            f.write(os.linesep)
            json.dump(doc, f)

    def get(self, kind, name):
        """Doc."""
        path = self._get_path(kind, name)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            return json.load(f)

    def delete(self, kind, name):
        """Doc."""
        path = self._get_path(kind, name)
        try:
            os.remove(path)
        except OSError:
            pass