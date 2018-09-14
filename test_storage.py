"""Unit tests for storage."""


from .storage import DocStore

ds = DocStore()


def test1():
    """Put then get."""
    ds.put(0, 1, {'test': 42})
    r = ds.get(0, 1)
    assert r['test'] == 42


def test2():
    """get none."""
    r = ds.get(99, 99)
    assert r == None
