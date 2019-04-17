
import pytest
import time
from app import app


@pytest.mark.parametrize('engine', 'zero'.split())
def test_full(engine):
    print('')
    app.testing = True
    tc = app.test_client()
    uid, pwd = 'marc@marc.com', 'marcdewdw'
    rv = tc.post('/login/{}'.format(uid), data={'email': uid, 'password': pwd})
    print(rv.json)
    rv = tc.get('/user_file/{}'.format(uid))
    print(rv.json)
    with open('test_data.csv', 'rb') as f:
        rv = tc.post('/upload/{}'.format(uid), data={'files[]': f})
        print(rv.status)
    rv = tc.get('/target/{}'.format(uid))
    print(rv.json)
    t = {'target': rv.json['target'].replace('Survivedp', 'Survivedt')}
    rv = tc.put('/target/{}'.format(uid), data=t)
    print(rv.json)
    rv = tc.post('/job/{}'.format(uid))
    print(rv.json)
    time.sleep(5)
    rv = tc.get('/result/{}'.format(uid))
    print(rv.json)
