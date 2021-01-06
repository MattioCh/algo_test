#%%

from zipline.api import (symbol, set_benchmark, order_target,
                         schedule_function, time_rules,order_value,order, set_max_leverage)
from zipline.finance import (commission,ledger)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from zipline.api import order_target, record, symbol
from zipline.finance import commission, slippage


def initialize(context):
    
    
    context.sym = symbol('AAPL')
    context.i = 1000

    print("HI")
    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    # Skip first 300 days to get full windows
    
    order(context.sym,context.i)
    print("Hi2")
    print(context.account.net_leverage," ", context.account.leverage)
    

    # Compute averages
    # history() has to be called with the same params
    # from above and returns a pandas dataframe.
    # short_mavg = data.history(context.sym, 'price', 100, '1d').mean()
    # long_mavg = data.history(context.sym, 'price', 300, '1d').mean()

    # # Trading logic
    # if short_mavg > long_mavg:
    #     # order_target orders as many shares as needed to
    #     # achieve the desired number of shares.
    #     order_target(context.sym, 100)
    # elif short_mavg < long_mavg:
    #     order_target(context.sym, 0)

    # # Save values for later inspection
    record(AAPL=data.current(context.sym, "price"))



# def analyze(context, perf):
#     fig = plt.figure(figsize=(12,8))
#     perf.algorithm_period_return.plot(x='strategy return', legend=True)
#     perf.benchmark_period_return.plot(legend=True)
#     plt.show()

# start = pd.Timestamp('2000-11-18', tz='utc')
# end = pd.Timestamp('2021-1-5', tz='utc')

# # Fire off backtest
# result = zipline.run_algorithm(
#     start=start, # Set start
#     end=end,  # Set end
#     initialize=initialize, # Define startup function
#     capital_base=100000000, # Set initial capital
#     data_frequency = 'daily',  # Set data frequency
#     bundle='custom-bundle' ) # Select bundle

# print("Ready to analyze result.")

#zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-5 -b custom-bundle --no-benchmark 
#zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 




# %%
