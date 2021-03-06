# -*- coding: utf-8 -*-
"""Introduction to forecasting Philippine stock prices.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xBwyVvX29YLW5v_RhtzImkqW6U9eIxJD
"""

!pip install pandas
!pip install datetime
!pip install fbprophet

import pandas as pd

jfc = pd.read_csv('jfc_20130901_to_20190426.csv')
jfc['CHART_DATE'] = pd.to_datetime(jfc.CHART_DATE)

jfc.tail()

jfc.set_index('CHART_DATE').CLOSE.plot(figsize=(15, 10))
plt.title('Jollibee Daily Closing Price', fontsize=25)

from fbprophet import Prophet
#Forecasting closing prices
ts = jfc[['CHART_DATE', 'CLOSE']]
ts.columns = ['ds', 'y']
ts.head()

HOLDOUT_START = '2019-03-01'

m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts[ts.ds < HOLDOUT_START])
future = m.make_future_dataframe(periods=7*4*12, freq='D')

pred = m.predict(future)

from matplotlib import pyplot as plt
fig1 = m.plot(pred)
plt.title('Jollibee: Forecasted Daily Closing Price', fontsize=25)

pred_holdout = pred[(pred.ds >= HOLDOUT_START)&(pred.ds <= ts.ds.max())].set_index('ds').yhat
target_holdout = ts[ts.ds >= HOLDOUT_START].set_index('ds')
comb = pd.concat([pred_holdout, target_holdout], axis=1).dropna()
comb

import numpy as np
rmse_holdout = np.sqrt(comb.yhat.subtract(comb.y).pow(2).mean())
rmse_holdout

mae_holdout = np.mean(np.abs(comb.yhat.subtract(comb.y)))
mae_holdout

comb.columns = ['Predicted', 'Actual']
comb.plot(figsize=(15, 10))
plt.title('Predicted vs Actual JFC Closing Price \n Validation Set RMSE: {}'.format(round(rmse_holdout, 2)), fontsize=25)

# Advanced diagnostics
from fbprophet.diagnostics import cross_validation
df_cv = cross_validation(m, initial=f'{ts.shape[0] - 30} days', horizon = '30 days')

from fbprophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
df_p['horizon_days'] = df_p.horizon.dt.days
df_p.set_index('horizon_days').mae.plot()

# Assess accuracy
import numpy as np

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mean_absolute_percentage_error(y_true, y_pred)

#Plotting returns of JFC
ts_pct = ts.set_index('ds').pct_change()
ts_pct.plot()

#Plotting log returns of JFC
import numpy as np

ts_pct = np.log(ts.set_index('ds').pct_change() + 1)
ts_pct.plot()

ts_pct.hist(bins=50)

m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts_pct.reset_index())
future = m.make_future_dataframe(periods=7*4*12, freq='D')

pred = m.predict(future)

from matplotlib import pyplot as plt
fig1 = m.plot(pred)
plt.title('Jollibee: Forecasted Daily Returns', fontsize=25)

#log first difference of JFC
import numpy as np

ts_pct = np.log(ts.set_index('ds')).diff()
ts_pct.plot()

ts_pct.hist(bins=50)

m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts_pct.reset_index())
future = m.make_future_dataframe(periods=7*4*12, freq='D')
pred = m.predict(future)

from matplotlib import pyplot as plt
fig1 = m.plot(pred)
plt.title('Jollibee: Forecasted Daily Returns', fontsize=25)

