#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 12:54:44 2018

@author: vanoudh
"""

import pandas as pd
from autosklearn.classification import AutoSklearnClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def run(path, target, return_dict):
    """Doc."""
    # path, target = input['path'], input['target']
    df = pd.read_csv(path)
    predictors = [v for v in target if target[v] == 'predictor']
    targets = [v for v in target if target[v] == 'target']
    X = df[predictors]
    y = df[targets[0]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    automl = AutoSklearnClassifier(time_left_for_this_task=100)
    automl.fit(X_train, y_train)
    y_hat = automl.predict(X_test)
    score = accuracy_score(y_test, y_hat)
    print("Accuracy score", score)
    return_dict['score'] = score
