# difference with logreg 
# 1. training every 30 days instead of only once 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from zipline.api import order_target, record, symbol, order_target_percent, set_max_leverage, get_open_orders, cancel_order
from zipline import run_algorithm
from zipline.finance import commission, blotter


# parameters 
lags = 3
training_period = 3500 # around 6-7 years
selected_stock = 'AAON'
n_stocks_to_buy = 1
short_ma_period = 20
inter_ma_period = 50
long_ma_period = 200

def initialize(context):
    context.time = 0
    context.asset = symbol(selected_stock)
    context.set_commission(commission.PerShare(cost=0.001, min_trade_cost=0))
    context.short_ma = 0
    #context.blotter = Blotter()

def handle_data(context, data):
    context.time += 1
    if context.time < training_period:
        return
    
    if context.time == training_period:
        print("One the 3500th day...")
        context.short_ma = data.history(context.asset, fields='price', bar_count = short_ma_period, frequency='1d').mean()
        #context.inter_ma = data.history(context.asset, fields='price', bar_count = inter_ma_period, frequency='1d').mean()
        #context.long_ma = data.history(context.asset, fields='price', bar_count = long_ma_period, frequency='1d').mean()
        print(context.short_ma)
        #print(context.long_ma)
        print("Out of 3500th day")
    
    if ((context.time - training_period) % 30 == 0): # retrain every 30 days
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

    # trading happens
    if context.time > training_period: # also when the retraining happens 
        lag_history = data.history(context.asset, fields='price', bar_count = lags+1, frequency="1d")
        ret = np.log(lag_history / lag_history.shift(1))  
        trend = context.model.predict(ret[1:].values.reshape(1,-1))

        if trend > 0:
            order_target_percent(context.asset, n_stocks_to_buy)
        elif trend < 0:
            order_target_percent(context.asset, -n_stocks_to_buy)

        short_ma = data.history(context.asset, fields='price', bar_count = short_ma_period, frequency='1d').mean()
        #inter_ma = data.history(context.asset, fields='price', bar_count = inter_ma_period, frequency='1d').mean()
        long_ma = data.history(context.asset, fields='price', bar_count = long_ma_period, frequency='1d').mean()

        # exit signals with moving average 
        if ((context.short_ma > long_ma) & (short_ma < long_ma )): # short descends through long
            print("exit sign")
            open_orders = get_open_orders(context.asset)
            for open_order in open_orders:
                if open_order['amount'] > 0:
                    cancel_order(open_order['id'])
                    print('cancelled')
            #print(open_orders)
            print("exit sign close")

        elif ((context.short_ma < long_ma) & (short_ma > long_ma)):
            print("exit sign2")
            open_orders = get_open_orders(context.asset)
            for open_order in open_orders:
                if open_order['amount'] < 0:
                    cancel_order(open_order['id'])
                    print('cancelled')
            #print(open_orders)
            print("exit sign 2 close")

        context.short_ma = short_ma      
        
        record(price=data.current(context.asset, 'price'))
        record(trend=trend)
        record(pnl=context.portfolio.pnl)
        record(shortma = short_ma)
        record(longma = long_ma)

def analyze(context, perf):
    fig, ax = plt.subplots(4, 1, sharex=True, figsize=[16,9])

    perf.portfolio_value.plot(ax=ax[0])
    ax[0].set_ylabel('portfolio value in $')

    perf['pnl'].plot(ax=ax[1])
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

result.to_pickle("test3.pkl")

'''
- closing positions
- more logic for combinations of long, short etc
- different lag
- different models in Logistic Regression
'''
# zipline run -f logreg.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle2 --no-benchmark --capital-base 100