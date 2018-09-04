"""Unit tests for storage."""


from .storage import DocStore

ds = DocStore()


def test1():
    """Put then get."""
    ds.put(0, 0, {'test': 42})
    r = ds.get(0, 0)
    assert r['test'] == 42
