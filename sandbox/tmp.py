
import pandas as pd

df = pd.read_csv('/home/vanoudh/Downloads/mlb/house_prices.csv')

s = """GrLivArea
LotArea
GarageArea
BsmtUnfSF
TotalBsmtSF
1stFlrSF
2ndFlrSF
TotRmsAbvGrd
OverallQual
OverallCond
BsmtQual
YearBuilt
YearRemodAdd
Neighborhood
SalePrice"""

cols = s.splitlines()

df[cols].to_csv('house_prices_simple.csv', index=False)