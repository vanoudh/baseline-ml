"""Created on Mon Jul  9 12:54:44 2018."""

import time
import pandas as pd
import sys
from automl import AutoSimple
from sklearn.model_selection import train_test_split
from storage_factory import ds, fs
from sklearn.metrics import accuracy_score, r2_score
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from sklearn.preprocessing import LabelEncoder
from utils import object_cols
from automl import get_type


def run(user_id, model):
    """Doc."""
    target = ds.get('target', user_id)
    print(target)
    path = fs.get_path('dataset', user_id)

    df = pd.read_csv(path)
    for c in object_cols(df):
        print(c)
        df[c] = df[c].fillna('NaN-Str')
        df[c] = LabelEncoder().fit_transform(df[c]) 
    
    predictors = [v for v in target if target[v] == 'predictor']
    targets = [v for v in target if target[v] == 'target']
    if len(predictors) == 0:
        raise ValueError('expecting at least one predictor')
    if len(targets) != 1:
        raise ValueError('expecting exactly one target')

    X = df[predictors]
    y = df[targets[0]]
    is_regressor, _ = get_type(y)

    print(X.head())
    print(y.head())

    AutoSklearn = AutoSklearnRegressor if is_regressor else AutoSklearnClassifier 
    scorer = r2_score if is_regressor else accuracy_score

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        random_state=1)
    
    if model == 'auto-sklearn':
        m = AutoSklearn(time_left_for_this_task=3600)
    else:
        m = AutoSimple(engine=model)

    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    score = scorer(y_test, y_pred)
    
    print("Score", score)
    ds.put('result-{}'.format(model), user_id, {'result': score})


if __name__ == '__main__':
    try:
        user_id, model = sys.argv[1], sys.argv[2]
        run(user_id, model)
    except Exception as e:
        message = '{}'.format(e)
        ds.put('result-{}'.format(model), user_id, {'result': message})
        raise e