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


model_list = [
    # (DummyRegressor(), True, False, 10, {
    #     'mo__strategy': ['mean', 'median']
    # }),
    # (DummyClassifier(), False, False, 10, {
    #     'mo__strategy': ['stratified', 'most_frequent', 'prior', 'uniform']
    # }),

    (AutoSklearnRegressor(), True, False, 1, {
        'mo__time_left_for_this_task': [100]
    }),
    (AutoSklearnClassifier(), False, False, 1, {
        'mo__time_left_for_this_task': [100]
    }),
]
