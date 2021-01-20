import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from zipline.api import order_target, record, symbol, order_target_percent, set_max_leverage
from zipline import run_algorithm
from zipline.finance import commission

# parameters 
lags = 3
training_period = 3500 # around 6-7 years
selected_stock = 'AAPL'
n_stocks_to_buy = 1

def initialize(context):
    context.time = 0
    context.asset = symbol(selected_stock)
    context.set_commission(commission.PerShare(cost=0.001, min_trade_cost=0))

def handle_data(context, data):
    context.time += 1
    if context.time < training_period:
        return
    
    if context.time == training_period: # train the model with historical data
        price_history = np.array(data.history(context.asset, fields="price", bar_count=training_period, frequency="1d"))
        cols = []
        df = pd.DataFrame(data=price_history, columns=['price'])
        df['return'] = np.log(df['price'] / df['price'].shift(1))
        for lag in range(1, lags+1):
            col = f'lag_{lag}'
            df[col] = df['return'].shift(lag)
            cols.append(col)
        df.dropna(inplace=True)
        lm = linear_model.LogisticRegression(C=1e7, solver='lbfgs', multi_class='auto', max_iter=1000)
        lm.fit(df[cols], np.sign(df['return']))
        context.model = lm
        #context.reg = np.linalg.lstsq(df[cols], df['return'], rcond=None)[0]
        #print(context.reg)

    # trading happens
    if context.time > training_period:
        lag_history = data.history(context.asset, fields='price', bar_count = lags+1, frequency="1d")
        ret = np.log(lag_history / lag_history.shift(1))        
        #trend = np.sign(np.dot(ret[1:], context.reg))
        trend = context.model.predict(ret[1:].values.reshape(1,-1))
        if trend > 0:
            order_target_percent(context.asset, n_stocks_to_buy)
            #print('buy')
        elif trend < 0:
            order_target_percent(context.asset, -n_stocks_to_buy)
            #print('sell')
        
        record(price=data.current(context.asset, 'price'))
        record(trend=trend)
        record(pnl=context.portfolio.pnl)

def analyze(context, perf):
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16,9])

    perf.portfolio_value.plot(ax=ax[0])
    ax[0].set_ylabel('portfolio value in $')

    perf['price'].plot(ax=ax[1])
    ax[1].set_ylabel('price in $')

    perf.returns.plot(ax=ax[2])
    ax[2].set_ylabel('daily returns')

    plt.legend()
    plt.show()
 
start = pd.Timestamp('2000-11-18', tz='utc')
end = pd.Timestamp('2021-1-4', tz='utc')

result = run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize,
    handle_data=handle_data, # Define startup function
    capital_base=100, # Set initial capital
    data_frequency = 'daily',  # Set data frequency
    bundle='custom-bundle2' # Select bundle
) 

result.to_pickle("test1.pkl")

'''
- closing positions
- more logic for combinations of long, short etc
- train everyday?
- train every 30 days?
- different lag
- different models in Logistic Regression
'''
# zipline run -f logreg.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle2 --no-benchmark --capital-base 100