"""Doc."""
import os
from google.cloud import datastore


project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
client = datastore.Client(project_id)

STORAGE_FOLDER = 'store'
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

    def _key(self, user_id, doc_id):
        return client.key(str(user_id), doc_id)

    def put(self, user_id, doc_id, doc, overwrite=False):
        """Doc."""
        entity = datastore.Entity(self._key(user_id, doc_id))
        
        if not overwrite and self.get(user_id, doc_id):
            raise FileExistsError('key exists already')

        for k, v in doc.items():        # entity.update(doc) ?
            entity[k] = v
        client.put(entity)

    def get(self, user_id, doc_id):
        """Doc."""
        return client.get(self._key(user_id, doc_id))
