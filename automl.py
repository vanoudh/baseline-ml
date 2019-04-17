# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 17:26:06 2018
@author: mvanoudh
"""

import logging
import numpy as np
import pandas as pd
import time
from numpy.random import seed

from category_encoders import OrdinalEncoder
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, check_cv
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.utils.multiclass import type_of_target
from sklearn.metrics.scorer import roc_auc_scorer, r2_scorer
from sklearn.preprocessing import Imputer
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.feature_selection import f_regression, f_classif
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor

from feature_extraction import DateEncoder, SparseCatEncoder
from feature_extraction import ConstantInputer, NumericFilter
from decomposition import TruncatedSVD2
from utils import TransformerWrap, PassThrought, numeric_cols, object_cols
from utils import model_name
from feature_selection import SelectKBest2
from feature_selection import f_forest_regression, f_linear_regression
from feature_selection import f_forest_classification, f_linear_classification
from metrics import avg_roc_auc_scorer

seed(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s')
logging.getLogger().setLevel(level=logging.INFO)

pd.options.display.width = 160


# Format is
# model_constructor, is_regressor, is_tree, max_try, { parameters }


_no_model = [
    (DummyRegressor(), True, False, 10, {
        'mo__strategy': ['mean', 'median']
    }),
    (DummyClassifier(), False, False, 10, {
        'mo__strategy': ['stratified', 'most_frequent']
    })
]

_linear_model = [
    (Ridge(), True, False, 10, {
        'mo__alpha': [1.0, 10]
    }),
    (LogisticRegression(), False, False, 10, {
        'mo__C': [1.0, 0.1]
    })
]

_tree_model = [
    (DecisionTreeRegressor(), True, True, 10, {
        'mo__criterion': ('mae', ),
        'mo__random_state': (0, )
    }),
    (DecisionTreeClassifier(), False, True, 10, {
        'mo__random_state': (0, )
    })
]

_forest_model = [
    (RandomForestRegressor(), True, True, 10, {
        'mo__criterion': ('mae', ),
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


def get_type(y):
    tot = type_of_target(y)
    if y.dtype != 'object' and len(np.unique(y)) > 100:
        tot = 'continuous'
    is_regressor = tot in ['continuous', 'continuous-multioutput']
    is_binary = tot == 'binary'
    return is_regressor, is_binary


def get_selector(is_regressor, is_tree):
    if is_regressor:
        return [mutual_info_regression]
    else:
        return [mutual_info_classif]


def get_pipeline(est, is_tree, is_regressor, params):
    name = model_name(est)
    if name.startswith('Dummy'):
        ppl = Pipeline([
                       ('ft', FunctionTransformer()),
                       ('mo', est)
                      ])
        params['ft__func'] = [lambda x:x[numeric_cols(x)]]
        params['ft__validate'] = [False]
    elif is_tree:
        ppl = Pipeline([
                       ('da', DateEncoder()),
                       ('oe', OrdinalEncoder()),
                       ('ft', FunctionTransformer()),
                       ('se', SelectKBest2()),
                       ('mo', est)
                      ])
        params['da__ascategory'] = [False]
        params['oe__drop_invariant'] = [True]
        params['ft__func'] = [lambda x:x.fillna(-999)]
        params['ft__validate'] = [False]
        params['se__score_func'] = get_selector(is_regressor, is_tree)
        params['se__k'] = [10000]
    else:
        # linear / knn
        ppl = Pipeline([
                ('da', DateEncoder()),
                ('en', FeatureUnion([
                       ('nu', Pipeline([('ft', FunctionTransformer()), ('in', Imputer()), ('sc', TransformerWrap(StandardScaler()))])),
                       ('ca', Pipeline([('ft', FunctionTransformer()), ('sc', SparseCatEncoder())]))
                       ])),
                ('fu', FeatureUnion([('se', SelectKBest2()), ('dr', TruncatedSVD2())])),
                ('mo', est)
                ])

        params['en__nu__ft__func'] = [lambda x:x[numeric_cols(x)]]
        params['en__nu__ft__validate'] = [False]
        params['en__ca__ft__func'] = [lambda x:x[object_cols(x)]]
        params['en__ca__ft__validate'] = [False]
        params['fu__se__score_func'] = get_selector(is_regressor, is_tree)
        params['fu__se__k'] = [10000]
        params['fu__dr__k'] = [0.3]

    return name, ppl, params


def get_pipelines(x, y, engine):
    is_regressor, _ = get_type(y)
    ppl_list = []
    model_list = model_factory(engine)
    for est, is_reg, is_tree, n_iter, params in model_list:
        if is_reg != is_regressor:
            continue
        name, ppl, params = get_pipeline(est, is_tree, is_regressor, params)
        ppl_list.append((name, ppl, params, n_iter))
    return ppl_list


def get_search_model(ppl, params, scorer, cv, n_iter, verbose):
    grid_size = len(ParameterGrid(params))
    logging.info('trying all {} configs'.format(grid_size))
    gs = GridSearchCV(ppl, params, scorer, cv=cv, verbose=verbose)
    # logging.debug('trying {} from {} configs'.format(n_iter, grid_size))
    # gs = RandomizedSearchCV(ppl, params, n_iter, scorer, cv=cv,
    #                         verbose=verbose, random_state=0)
    return gs


def get_cv(cv, y):
    if not isinstance(cv, str):
        return cv
    sep = ':'
    if cv.find(sep) < 0:
        cv += sep + '3'
    cvtype, n = cv.split(sep)
    if cvtype != 'ts':
        raise ValueError('unexpected type:' + cvtype)
    return TimeSeriesSplit(n_splits=int(n))


def get_search_models(x, y, scorer, cv, iter_factor, 
                      engine, verbose):
    ppl_list = get_pipelines(x, y, engine)
    cv = get_cv(cv, y)
    for name, ppl, params, n_iter in ppl_list:
        yield name, get_search_model(ppl,
                                     params,
                                     scorer,
                                     cv,
                                     max(int(n_iter*iter_factor), 1),
                                     verbose)


def get_best_model(x, y, scorer=None, cv=None, iter_factor=1, 
                   engine='auto-sklearn', verbose=0):
    best_sm = None
    sms = get_search_models(x, y, scorer, cv, iter_factor, 
                            engine, verbose)
    for name, sm in sms:
        if verbose > 0:
            logging.info('{} starting...'.format(name))
        sm.fit(x, y)
        if best_sm is None or sm.best_score_ > best_sm.best_score_:
            best_sm = sm
        logging.info('{:>24} test score : {:.4f}'.format(name, sm.best_score_))
    return best_sm


class AutoSimple:
    def __init__(self, 
                 scorer=None, 
                 cv=None,   
                 iter_factor=1, 
                 engine='zero'):
        self.scorer = scorer
        self.cv = cv
        self.iter_factor = iter_factor
        self.engine = engine
        self.model = None
    
    def fit(self, x, y, verbose=0):
        self.model = get_best_model(x, y,
                                    self.scorer,
                                    self.cv,
                                    self.iter_factor,
                                    self.engine,
                                    verbose)
        return self.model

    def predict(self, x):
        return self.model.predict(x)
