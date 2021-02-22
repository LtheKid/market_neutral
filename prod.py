import pandas as pd
import pandas_datareader
from pandas_datareader import get_data_yahoo as yh
import itertools

# Define variables and inputs:
asset_count=5
ma_short=15
ma_long=50
pv_period=5


myassetlist = input('Assets here, separated by commas: ')
myassetlist = myassetlist.split(',')

use_internal_data = input('Use Internal Data csv file? - reply y/n: ')


if use_internal_data == 'y':
    df = pd.read_csv('data.csv')[myassetlist]
else:
    df = yh(myassetlist)['Close'] # Get close prices
    df.combine_first(pd.read_csv('data.csv', index_col = 'Date', parse_dates=True)).to_csv('data.csv') #update local data source
    

# Get 20 day returns and rank
ranked_momentum = pd.DataFrame(df.pct_change(20).mean().sort_values(ascending = False)) # Ascending to descending returns
ranked_momentum.columns = ['20_day_returns']
ranked_momentum['rank'] = ranked_momentum['20_day_returns'].rank()
ranked_momentum

#moving average short/long term
# (short ma - long ma) / long ma
ranked_ma_assets = pd.DataFrame(((df.tail(ma_short).mean()-df.tail(ma_long).mean())/df.tail(ma_long).mean()).sort_values(ascending = False))
ranked_ma_assets.columns = ['MA_crossover']
ranked_ma_assets['rank'] = ranked_ma_assets.rank()
ranked_ma_assets

#VPT indicator
# Reference: https://www.investopedia.com/terms/v/vptindicator.asp

vf=yh(myassetlist)['Volume']
ranked_pv_assets = pd.DataFrame(((vf*df.pct_change()).cumsum()).pct_change(pv_period).tail(1).sum().sort_values(ascending = False))
ranked_pv_assets

ranked_pv_assets.columns = ['VPT_Indicator']
ranked_pv_assets['rank'] = ranked_pv_assets.rank()
ranked_pv_assets

combined = pd.DataFrame(pd.concat([ranked_momentum,ranked_ma_assets,ranked_pv_assets])['rank'])
combined = combined.reset_index()
combined.columns=['Symbols','rank']
combined = combined.groupby('Symbols').sum().sort_values('rank',ascending=False)

print('Results')
print(combined)
combined.sort_values(by='rank').plot.bar(figsize=(20,15), fontsize=20, rot=0)
