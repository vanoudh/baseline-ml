"""Created on Mon Jul  9 12:54:44 2018."""

import logging
import time
import pandas as pd
import sys

from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.metrics.scorer import accuracy_scorer, neg_mean_absolute_error_scorer
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from sklearn.preprocessing import LabelEncoder

from automl import get_type, AutoSimple

from sklearn.model_selection import train_test_split
from storage_factory import ds, fs, put_result
from utils import object_cols, read_csv, round3
from app import MODEL_LIST


class Runner:

    def prepare(self, user_id):
        filename = ds.get('file', user_id)['filename']
        target = ds.get('target', user_id)['target'].split(',')
        path = fs.get_path(filename)
        self.df = read_csv(path)

        self.predictors = [v[0:-1] for v in target if v[-1] == 'p']
        self.targets = [v[0:-1] for v in target if v[-1] == 't']

        if len(self.predictors) == 0:
            raise ValueError('Expecting at least one predictor')
        if len(self.targets) != 1:
            raise ValueError('Expecting exactly one target')
        

    def run(self, user_id, model, shuffle):

        df = self.df.copy()
        nmax = 10 if model == 'linear' else 0
        for c in object_cols(self.df):
            df[c] = df[c].fillna('NaN')
            if df[c].nunique() > nmax:
                df[c] = LabelEncoder().fit_transform(df[c]) 

        X = df[self.predictors]
        y = df[self.targets[0]]

        # HACK to keep sklearn happy
        if model in 'zero linear'.split():
            if len(object_cols(X)) == len(X.columns):
                X = X.copy()
                X['one'] = 1

        if y.name in object_cols(self.df):
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
                                                            test_size=0.2,
                                                            shuffle=shuffle)
        
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

    runner = Runner()
    user_id, model = sys.argv[1], sys.argv[2]
    mlist = [model] if model in MODEL_LIST else MODEL_LIST

    try:
        runner.prepare(user_id)
        for m in mlist:
            try:
                runner.run(user_id, m, False)
            except Exception as e:
                logging.error(e)
                message = '{}'.format(e)
                put_result(m, user_id, 'error', message)
    except Exception as e:
        logging.error(e)
        message = '{}'.format(e)
        for m in mlist:
            put_result(m, user_id, 'error', message)
 