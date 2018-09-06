"""Doc."""
import os
import json

STORAGE_FOLDER = '/home/vanoudh/dev/mlb/store'
S = '-'

if not os.path.isdir(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)


class FileStore:
    """Doc."""

    def save(self, user_id, file_id, file):
        """Doc."""
        path = self.get_path(user_id, file_id)
        file.save(path)

    def get_path(self, user_id, file_id):
        """Doc."""
        li = [str(user_id), str(file_id)]
        return os.path.join(STORAGE_FOLDER, S.join(li))


class DocStore:
    """Doc."""

    def get_path(self, user_id, doc_id):
        """Doc."""
        li = [str(user_id), str(doc_id), 'json']
        return os.path.join(STORAGE_FOLDER, S.join(li))

    def put(self, user_id, doc_id, doc, overwrite=False):
        """Doc."""
        path = self.get_path(user_id, doc_id)
        if not overwrite:
            if os.path.isfile(path):
                raise FileExistsError(path)
        with open(path, 'w') as f:
            json.dump(doc, f)

    def get(self, user_id, doc_id):
        """Doc."""
        path = self.get_path(user_id, doc_id)
        if not os.path.isfile(path):
            return None
        with open(path) as f:
            return json.load(f)
