import os
import logging

if os.getenv('LOCAL') == 'yes':
    logging.warn('Using storage mock')
    from storageapi_mock import FileStore, DocStore
else:
    logging.warn('Using google datastore')
    from storageapi import FileStore, DocStore

fs = FileStore()
ds = DocStore()


def put_result(model, user_id, status, value):
    p = {'status': status, 'value': value}
    ds.put('result_{}'.format(model), user_id, p)


def get_result(model, user_id):
    return ds.get('result_{}'.format(model), user_id)