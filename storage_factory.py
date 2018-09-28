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

