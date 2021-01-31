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
ranked_assets = pd.DataFrame(df.pct_change(20).mean().sort_values(ascending = False)) # Ascending to descending returns
ranked_assets # full assets

#moving average short/long term
ranked_ma_assets = pd.DataFrame(((df.tail(ma_short).mean()-df.tail(ma_long).mean())/df.tail(ma_long).mean()).sort_values(ascending = False))
ranked_ma_to_trade = pd.concat([ranked_ma_assets.head(asset_count),ranked_ma_assets.tail(asset_count)])
ranked_ma_to_trade['Direction']= -1
for row in ranked_ma_to_trade.head(asset_count):
    ranked_ma_to_trade.head(asset_count)['Direction']= 1
ranked_ma_to_trade.columns = ['MA_strategy','Direction']
# ranked_ma_to_trade

#Price ratio
#list(itertools.combinations(myassetlist, 2))

#VPT indicator
vf=yh(myassetlist)['Volume']
ranked_pv_assets = pd.DataFrame(((vf*df.pct_change()).cumsum()).pct_change(pv_period).tail(1).sum().sort_values(ascending = False))
ranked_pv_to_trade = pd.concat([ranked_pv_assets.head(asset_count),ranked_pv_assets.tail(asset_count)])
ranked_pv_to_trade['Direction']= -1
for row in ranked_pv_to_trade.head(asset_count):
    ranked_pv_to_trade.head(asset_count)['Direction']= 1
ranked_pv_to_trade.columns = ['VPT_strategy','Direction']
# ranked_pv_to_trade

long = ranked_assets[0:asset_count] # top 2 assets
long['Direction'] = 1
long.columns = ['20_day_returns','Direction']
# long

short = ranked_assets[-asset_count:] # bottom 2 assets
short['Direction'] = -1
short.columns = ['20_day_returns','Direction']
# short

assets_to_trade = pd.concat([long,short])

combined = pd.DataFrame(pd.concat([assets_to_trade,ranked_ma_to_trade,ranked_pv_to_trade])['Direction'])
combined = combined.reset_index()
combined = combined.groupby('Symbols').sum()

print('Results')
print(combined)
combined.sort_values(by='Direction').plot.bar(figsize=(20,15), fontsize=20, rot=0)
