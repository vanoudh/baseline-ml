# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:31:35 2018
@author: mvanoudh
"""

import numpy as np
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier

from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor

# Format is
# model_constructor, is_regressor, is_tree, max_try, { parameters }


_no_model = [
    (DummyRegressor(), True, False, 10, {
        'mo__strategy': ['mean', 'median']
    }),
    (DummyClassifier(), False, False, 10, {
        'mo__strategy': ['stratified', 'most_frequent', 'prior', 'uniform']
    })
]

_linear_model = [
    (Ridge(), True, False, 10, {
    }),
    (LogisticRegression(), False, False, 10, {
    })
]

_tree_model = [
    (DecisionTreeRegressor(), True, True, 10, {
        'mo__random_state': (0, )
    }),
    (DecisionTreeClassifier(), False, True, 10, {
        'mo__random_state': (0, )
    })
]

_forest_model = [
    (RandomForestRegressor(), True, True, 10, {
        'mo__random_state': (0, )
    }),
    (RandomForestClassifier(), False, True, 10, {
        'mo__random_state': (0, )
    })
]


def model_factory(engine):
    if engine == 'zero':
        return _no_model
    if engine == 'linear':
        return _linear_model
    if engine == 'tree':
        return _tree_model
    if engine == 'forest':
        return _forest_model
    raise ValueError('unknown engine :{}'.format(engine))

