import os
import logging

if os.getenv('LOCAL') == 'yes':
    logging.info('using storage mock')
    from .storageapi_mock import FileStore, DocStore
else:
    from .storageapi import FileStore, DocStore

fs = FileStore()
ds = DocStore()

