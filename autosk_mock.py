#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 12:54:44 2018.

@author: vanoudh
"""

import pandas as pd
import sys
import time

from storage import DocStore, FileStore


ds = DocStore()
fs = FileStore()


def run(user_id, mode):
    """Doc."""
    target = ds.get(user_id, 'target')
    path = fs.get_path(user_id, 'dataset')
    df = pd.read_csv(path)
    predictors = [v for v in target if target[v] == 'predictor']
    targets = [v for v in target if target[v] == 'target']
    X = df[predictors]
    y = df[targets[0]]
    print(X.head())
    print(y.head())
    time.sleep(5)
    ds.put(user_id, 'result', {'auto-sklearn-mock': 0})


run(sys.argv[1])
