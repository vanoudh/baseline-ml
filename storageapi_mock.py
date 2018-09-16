"""Doc."""
import os
import json

STORAGE_FOLDER = '.store_mock'
S = '-'

if not os.path.isdir(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)


class FileStore:
    """Doc."""

    def save(self, kind, name, file):
        """Doc."""
        path = self.get_path(kind, name)
        file.save(path)

    def get_path(self, kind, name):
        """Doc."""
        li = [str(kind), str(name)]
        return os.path.join(STORAGE_FOLDER, S.join(li))


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
        return os.remove(path) 