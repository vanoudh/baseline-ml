"""Created on Mon Jul  9 12:54:44 2018."""

import logging
import time
import pandas as pd
import sys


from automl import AutoSimple
from sklearn.model_selection import train_test_split
from storage_factory import ds, fs, put_result
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.metrics.scorer import accuracy_scorer, neg_mean_absolute_error_scorer
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from sklearn.preprocessing import LabelEncoder
from utils import object_cols, read_csv, round3
from automl import get_type



def run(user_id, model):
    """Doc."""
    filename = ds.get('file', user_id)['filename']
    target = ds.get('target', user_id)['target'].split(',')
    path = fs.get_path(filename)

    # print('target', target)

    df = read_csv(path)
    if model == 'auto-sklearn':
        for c in object_cols(df):
            df[c] = df[c].fillna('NaN-Str')
            df[c] = LabelEncoder().fit_transform(df[c]) 
        
    predictors = [v[0:-1] for v in target if v[-1] == 'p']
    targets = [v[0:-1] for v in target if v[-1] == 't']

    # print('pred', predictors)
    # print('targ', targets)

    if len(predictors) == 0:
        raise ValueError('Expecting at least one predictor')
    if len(targets) != 1:
        raise ValueError('Expecting exactly one target')

    X = df[predictors]
    y = df[targets[0]]

    print(y.name, y.dtype, y.isnull().sum())
    if y.name in object_cols(df):
        y = y.fillna('NaN')
    else:
        y = y.fillna(0)

    is_regressor, _ = get_type(y)
        
    AutoSklearn = AutoSklearnRegressor if is_regressor else AutoSklearnClassifier 
    score_func = mean_absolute_error if is_regressor else accuracy_score
    scorer = neg_mean_absolute_error_scorer if is_regressor else accuracy_scorer
    
    if model == 'zero':
        score_desc = 'Mean Absolute Error' if is_regressor else 'Accuracy'
        ds.put('score_desc', user_id, {'score_desc': score_desc})

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=0.8,
                                                        shuffle=False)
    
    if model == 'auto-sklearn':
        m = AutoSklearn(time_left_for_this_task=600)
    else:
        m = AutoSimple(engine=model, scorer=scorer)

    put_result(model, user_id, 'running', 'learning...')

    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    score = score_func(y_test, y_pred)

    # X_shuffle = X_test.copy()
    # for c in X_shuffle.columns:
    #     tmp = X_shuffle[c]
    #     X_shuffle[c] = X_shuffle[c].sample(frac=1).values
    #     print(c, score_func(y_test, m.predict(X_shuffle)))
    #     X_shuffle[c] = tmp
    
    logging.info("Score {}".format(score))
    put_result(model, user_id, 'ok', round3(score))

if __name__ == '__main__':
    try:
        user_id, model = sys.argv[1], sys.argv[2]
        run(user_id, model)
    except Exception as e:
        logging.error(e)
        message = '{}'.format(e)
        put_result(model, user_id, 'error', message)