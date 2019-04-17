
import pytest
from automl import AutoSimple

from datasets import get_iris, get_boston



@pytest.mark.parametrize('engine', 'zero linear tree'.split())
def test_classif_all_numeric(engine):
    x, y = get_iris(True)
    print(AutoSimple(engine=engine).fit(x, y).predict(x))


@pytest.mark.parametrize('engine', 'tree forest'.split())
def test_classif_all_string(engine):
    x, y = get_iris(True)
    for c in x.columns:
        x[c] = x[c].astype(str)
    print(AutoSimple(engine=engine).fit(x, y).predict(x))


# def test_classif_all_cat():
#     x, y = get_iris(True)
#     for engine in 'zero tree linear'.split():
#         print(AutoSimple(engine=engine).fit(x, y).predict(x))


# import pytest

# @pytest.mark.parametrize('arg', 'toto tutu'.split())
# def test_pp(arg):
#     assert 'toto' == arg