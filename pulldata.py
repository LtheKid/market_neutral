import pandas as pd
from pandas_datareader import get_data_yahoo as yh

df = yh(['GME','AAPL','TSLA','TLT','SPY','QQQ','UGL','GLD','TMF')['Close']
df.to_csv("data.csv")



