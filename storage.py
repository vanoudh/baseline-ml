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

    def put(self, user_id, doc_id, doc):
        """Doc."""
        print('put', doc)
        entity = datastore.Entity(self._key(user_id, doc_id))        
        entity.update(doc)
        client.put(entity)

    def get(self, user_id, doc_id):
        """Doc."""
        r = client.get(self._key(user_id, doc_id))
        if r is None:
            return r
        doc = {}
        for k, v in r.items():
            doc[k] = v
        print('get', doc)
        return doc

    def delete(self, user_id, doc_id):
        """Doc."""
        return client.delete(self._key(user_id, doc_id))

