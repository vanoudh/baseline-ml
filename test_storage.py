"""Unit tests for storage."""

import pytest
import secrets
from .storage import DocStore

ds = DocStore()
id = secrets.token_hex(8)
key = secrets.token_hex(8)


def test1():
    """Put, get, delete."""
    ds.put(id, key, {'test': 42})
    r = ds.get(id, key)
    assert r['test'] == 42
    ds.delete(id, key)
    assert ds.get(id, key) == None

js = {
    "PassengerId": "predictor", "Survived": "target", 
    "Pclass": "predictor", "Sex": "predictor", 
    "Age": "predictor", "Fare": "predictor"}

def test2():
    """Put then get."""
    ds.put(id, key, js)
    r = ds.get(id, key)
    assert r['PassengerId'] == 'predictor'
    assert r['Survived'] == 'target'
    assert r == js
    print(r)
    ds.delete(id, key)
    assert ds.get(id, key) == None

# test2()

