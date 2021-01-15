import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from zipline.api import order_target, record, symbol, order_target_percent, set_max_leverage
from zipline.finance import commission

# parameters 
ma_periods = 20
selected_stock = 'DBC'
n_stocks_to_buy = 10

def initialize(context):
    context.time = 0
    context.asset = symbol(selected_stock)
    context.set_commission(commission.PerShare(cost=0.001, min_trade_cost=0))

def handle_data(context, data):
    context.time += 1
    if context.time < ma_periods:
        return
    
    price_history = data.history(context.asset, fields="price", bar_count=ma_periods, frequency="1d")
    ma = price_history.mean()

    if (price_history[-2] < ma) & (price_history[-1] > ma):
        order_target(context.asset, n_stocks_to_buy)
    elif (price_history[-2] > ma) & (price_history[-1] < ma):
        order_target(context.asset, 0)
    
    record(price=data.current(context.asset, 'price'),
            moving_average=ma)

def analyze(context, perf):
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16, 9])

    perf.portfolio_value.plot(ax=ax[0])
    ax[0].set_ylabel('portfolio value in $')

    perf[['price', 'moving_average']].plot(ax=ax[1])
    ax[1].set_ylabel('price in $')

    perf_trans = perf.loc[[t != [] for t in perf.transactions]]
    buys = perf_trans.loc[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.loc[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax[1].legend()

    perf.returns.plot(ax=ax[2])
    ax[2].set_ylabel('daily returns')

    plt.legend()
    plt.show()