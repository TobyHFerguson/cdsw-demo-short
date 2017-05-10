# Google Stock Analytics
# ======================
#
# This notebook implements a strategy that uses Google Trends data to
# trade the Dow Jones Industrial Average.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas_highcharts.display import display_charts
import seaborn
mpl.rcParams['font.family'] = 'Source Sans Pro'
mpl.rcParams['axes.labelsize'] = '16'

# Ensure we're in the correct directory
import os
if (os.getcwd() != '/home/cdsw/cdsw-demo-short'):os.chdir("cdsw-demo-short")

# Import Data
# ===========
#
# Load data from Google Trends.

data = pd.read_csv('data/GoogleTrendsData.csv', index_col='Date', parse_dates=True)
data.head()

# Show DJIA vs. debt related query volume.
display_charts(data, chart_type="stock", title="DJIA vs. Debt Query Volume", secondary_y="debt")
seaborn.lmplot("debt", "djia", data=data, size=7)

# Detect if search volume is increasing or decreasing in
# any given week by forming a moving average and testing if the current value
# crosses the moving average of the past 3 weeks.
#
# Let's first compute the moving average.

data['debt_mavg'] = data.debt.rolling(window=3, center=False).mean()
data.head()

# Since we want to see if the current value is above the moving average of the
# *preceeding* weeks, we have to shift the moving average timeseries forward by one.

data['debt_mavg'] = data.debt_mavg.shift(1)
data.head()

# Generate Orders
# ===============
#
# We use Google Trends to determine how many searches have been
# carried out for a specific search term such as debt in week,
# where Google defines weeks as ending on a Sunday, relative to the total
# number of searches carried out on Google during that time.
#
# We implement the strategy of selling when debt searchess exceed
# the moving average and buying when debt searchers fall below the moving
# average.

data['order'] = 0
data.loc[data.debt > data.debt_mavg, 'order'] = -1
data.loc[data.debt < data.debt_mavg, 'order'] = -1
data.head()

# Compute Returns
# ===============

data['ret_djia'] = data.djia.pct_change()
data.head()

# Returns at week `t` are relative to week `t-1`. However, we are buying at
# week `t` and selling at week `t+1`, so we have to adjust by shifting
# the returns upward.

data['ret_djia'] = data['ret_djia'].shift(-1)

# The algorithm that is used by the authors makes a decision every Monday of
# whether to long or short the Dow Jones. After this week passed, we exit all
# positions (sell if we longed, buy if we shorted) and make a new trading0
# decision.
#
# The $ret$ column contains the weekly returns. Thus, if we buy at week $t$ sell
# at week $t+1$ we make the returns of week $t+1$. Conversely, if we short at
# week $t$ and buy back at week $t+1$ we make the negative returns of week $t+1$."

data['ret_google'] = data.order * data.ret_djia
data['cumulative_google'] = data.ret_google.cumsum()
data['cumulative_djia'] = data.ret_djia.cumsum()

display_charts(data[["cumulative_google", "cumulative_djia"]], 
               title="Cumulative Return for DJIA vs. Google Strategy")
