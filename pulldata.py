import pandas as pd
from pandas_datareader import get_data_yahoo as yh

df = yh(['GME','AAPL'])['Close']
df.to_csv("data.csv")



