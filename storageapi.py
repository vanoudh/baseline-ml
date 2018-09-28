"""Doc."""
import os
import json
import logging
from google.cloud import storage
from google.cloud import datastore
import secrets

STORAGE_FOLDER = '.store_cache'
S = '-'

if not os.path.isdir(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
logging.info('project id {}'.format(project_id))

sc = storage.Client(project_id)
BUCKET = '{}-media'.format(project_id)
bucket = sc.get_bucket(BUCKET)

dc = datastore.Client(project_id)


class FileStore:
    """Doc."""

    def save(self, filename, file):
        """Doc."""
        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

    def get_path(self, filename):
        """Doc."""
        blob = bucket.blob(filename)
        sec = secrets.token_hex(4//2)
        path = os.path.join(STORAGE_FOLDER, sec + filename)
        blob.download_to_filename(path)
        return path


class DocStore:
    """Doc."""

    def _key(self, kind, name):
        return dc.key(kind, name)

    def put(self, kind, name, doc):
        """Doc."""
        entity = datastore.Entity(self._key(kind, name))        
        entity.update(doc)
        dc.put(entity)

    def log(self, kind, doc):
        """Doc."""
        entity = datastore.Entity(dc.key(kind))        
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
        return doc

    def delete(self, kind, name):
        """Doc."""
        dc.delete(self._key(kind, name))

        