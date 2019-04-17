"""Unit tests for storage."""

import logging
import pytest
import secrets
from storage_factory import ds

kind = 'utest'
name = secrets.token_hex(4//2)


js = {
    "PassengerId": 1, 
    "Survived": "target", 
    "Pclass": "predictor", 
    "Sex": "predictor", 
    "Fare": "predictor"
    }

def test1():
    """Put, get, delete."""
    ds.put(kind, name, js)
    r = ds.get(kind, name)
    assert r['PassengerId'] == 1
    assert r['Survived'] == 'target'
    assert r == js
    logging.info(r)
    ds.delete(kind, name)
    assert ds.get(kind, name) == None


js = {
    "PassengerId": 1, 
    "Survived": "target", 
    "Pclass": {'a': 3}, 
    "Sex": "predictor" 
    }

def test2():
    """Put, get, delete."""
    ds.put(kind, name, js)
    r = ds.get(kind, name)
    assert r['Pclass']['a'] == 3
    assert r == js
    logging.info(r)
    ds.delete(kind, name)
    assert ds.get(kind, name) == None


