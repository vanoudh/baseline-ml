import os

if os.getenv('LOCAL'):
    print('using storage mock')
    from .storageapi_mock import FileStore, DocStore
else:
    from .storageapi import FileStore, DocStore

fs = FileStore()
ds = DocStore()

