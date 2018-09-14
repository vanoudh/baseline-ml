"""Unit tests for storage."""

import pytest
import secrets
from .storage import DocStore

ds = DocStore()
id = secrets.token_hex(8)
key = secrets.token_hex(8)


js = {
    "PassengerId": 1, 
    "Survived": "target", 
    "Pclass": "predictor", 
    "Sex": "predictor", 
    "Fare": "predictor"
    }

def test1():
    """Put, get, delete."""
    ds.put(id, key, js)
    r = ds.get(id, key)
    assert r['PassengerId'] == 1
    assert r['Survived'] == 'target'
    assert r == js
    print(r)
    ds.delete(id, key)
    assert ds.get(id, key) == None


js = {
    "PassengerId": 1, 
    "Survived": "target", 
    "Pclass": {'a': 3}, 
    "Sex": "predictor", 
    "Fare": "predictor"
    }

def test2():
    """Put, get, delete."""
    ds.put(id, key, js)
    r = ds.get(id, key)
    assert r['Pclass']['a'] == 3
    assert r == js
    print(r)
    ds.delete(id, key)
    assert ds.get(id, key) == None


