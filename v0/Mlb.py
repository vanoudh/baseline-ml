
import pandas as pd
import time

class Mlb:

    def prerun(self, filename):
        df = pd.read_csv(filename, sep=',')
        return df.columns

    def run(self, filename, x_cols, y_col):
        time.sleep(0.5)
        return filename + ' ' + str(x_cols) + ' ' + str(y_col)
