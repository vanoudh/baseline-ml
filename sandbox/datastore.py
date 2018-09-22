import os
import json
import logging
from datetime import datetime

from google.cloud import storage
from google.cloud import datastore

logging.getLogger().setLevel(logging.INFO)

S = '-'

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
logging.info('project id {}'.format(project_id))

# sc = storage.Client(project_id)
# BUCKET = '{}-media'.format(project_id)
# bucket = sc.get_bucket(BUCKET)

# dc = datastore.Client(project_id)

# kind = 'event'

# for i in range(1):
#     entity = datastore.Entity(dc.key(kind))        
#     entity.update({'user': 'marc', 'action': 'login', 'time': datetime.now()})
#     dc.put(entity)