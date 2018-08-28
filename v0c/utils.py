"""Doc."""
import pandas as pd


def summary(df):
    """Doc."""
    pres = pd.DataFrame()
    pres['nulls'] = df.isnull().sum()
    pres['unique'] = df.nunique()
    pres['type'] = df.dtypes
    pres['mode'] = df.mode(axis=0).iloc[0]
    pres['median'] = df.median()
    return pres
