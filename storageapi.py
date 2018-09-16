"""Doc."""
import os
import json
from google.cloud import storage
from google.cloud import datastore

STORAGE_FOLDER = '.store_cache'
S = '-'

if not os.path.isdir(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
print('project id {}'.format(project_id))

sc = storage.Client(project_id)
BUCKET = '{}-media'.format(project_id)
bucket = sc.get_bucket(BUCKET)

dc = datastore.Client(project_id)


class FileStore:
    """Doc."""

    def save(self, kind, name, file):
        """Doc."""
        filename = self._get_filename(kind, name)
        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

    def _get_filename(self, kind, name):
        """Doc."""
        li = [str(kind), str(name)]
        return S.join(li)

    def get_path(self, kind, name):
        """Doc."""
        filename = self._get_filename(kind, name)
        blob = bucket.blob(filename)
        path = os.path.join(STORAGE_FOLDER, filename)
        blob.download_to_filename(path)
        return path


class DocStore:
    """Doc."""

    def _key(self, kind, name):
        return dc.key(kind, name)

    def put(self, kind, name, doc):
        """Doc."""
        print('put', doc)
        entity = datastore.Entity(self._key(kind, name))        
        entity.update(doc)
        dc.put(entity)

    def get(self, kind, name):
        """Doc."""
        r = dc.get(self._key(kind, name))
        if r is None:
            return r
        doc = {}
        for k, v in r.items():
            doc[k] = v
        print('get', doc)
        return doc

    def delete(self, kind, name):
        """Doc."""
        return dc.delete(self._key(kind, name))
