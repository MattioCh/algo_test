
from zipline import run_algorithm
from zipline.api import *
from zipline.finance import commission, slippage
from scipy.stats import kendalltau
from scipy.stats import linregress
from zipline.finance import (commission)
from statsmodels.distributions.empirical_distribution import ECDF
import operator
from copulas.bivariate import Bivariate

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from helper import find_Return,compare_array_with_float

def initialize(env):
    # set_max_leverage(3.3)
    set_benchmark(False)
    env.capital_base = 100000
    env.sym = [symbol("NSC"),symbol("CSX")]
    env.day_count = 0
    env.floor_CL = 0.05
    env.cap_CL = 0.95
    env.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    env.set_slippage(slippage.VolumeShareSlippage())
    env.leverage_flag = 0
    env.model = ""
    env.long_short_percentage = 1
    env.hold_flag = 0
    pass



def handle_data(env, data):
    # Skip first 1000 days to get full windows
    if env.day_count < 1001:
        env.day_count +=1
        return

        # trading happens 
    else:
        df = data.history(env.sym , "close", bar_count = env.day_count, frequency = "1d")

        #                     columns
        # index   |---AAPL--- | --stock 2---
        # time1           1               2
        # time2           8               6
        # time3           4               7
        
        # df.indexes ->> [time1, time2,time3]
        # df.columns -->> [stock1,stock2]
        # df.loc[:,["AAPL","MSFT"]]


        print("--------------------------------")
        print(df.index[-1])
        ret = find_Return(df)
        ret_1 = ret.iloc[:,0]
        ret_2 = ret.iloc[:,1]
        # ret_1 = ret_1/ret_1.std()
        # ret_2 = ret_1/ret_2.std()

        tau_ = kendalltau(ret_1,ret_2)[0]

        if env.day_count % 1000 == 1:
            u = ECDF(ret_1)(ret_1) 
            v = ECDF(ret_2)(ret_2)
            u_v_stack = np.vstack((u,v)).T
            env.model = Bivariate().select_copula(u_v_stack)
            
        u = ECDF(ret_1)(ret_1[-2:]) 
        v = ECDF(ret_2)(ret_2[-2:])
        u_v_stack = np.vstack((u,v)).T
        v_u_stack = np.vstack((v,u)).T

        # Misprice index 


        MI_u_v = env.model.partial_derivative(u_v_stack)[-2:]
        MI_v_u = env.model.partial_derivative(v_u_stack)[-2:]

        # Trading logic 
        if env.leverage_flag == 0:
            if compare_array_with_float(MI_u_v, env.floor_CL,"<") and compare_array_with_float(MI_v_u, env.cap_CL,">"):
                #long u short v
                long_pos = order_target_percent(env.sym[0], env.long_short_percentage)
                short_pos = order_target_percent(env.sym[1], -env.long_short_percentage )
                print(-116)

            # Placing orders: if short is relatively underpriced, sell the pair
            elif compare_array_with_float(MI_u_v, env.cap_CL,">") and compare_array_with_float(MI_v_u, env.floor_CL,"<"):
                #short u long v
                long_pos = order_target_percent(env.sym[1], env.long_short_percentage )
                short_pos = order_target_percent(env.sym[0], -env.long_short_percentage )
                print(-123)
            else:
                short_pos = order_target(env.sym[1], 0)
                long_pos = order_target(env.sym[0], 0)
                print(-127)
            env.leverage_flag = 1 if env.account.net_leverage > 3  else 0
            pass

        else:
            if (compare_array_with_float(MI_u_v, env.floor_CL,">") and compare_array_with_float(MI_v_u, env.cap_CL,"<")) or (compare_array_with_float(MI_u_v, env.cap_CL,"<") and compare_array_with_float(MI_v_u, env.floor_CL,">")):
                short_pos = order_target(env.sym[1], 0)
                long_pos = order_target(env.sym[0], 0)
                env.leverage_flag = 0 if env.account.net_leverage < 3 else 1
                print(-137)
                pass
            pass
        
        print("P1: ",df.iloc[-1,0])
        print("P2: ",df.iloc[-1,1])
        print("PNL: ", env.portfolio.pnl)
        # print("coef:",coef)
        print(u)
        print(v)
        print(MI_u_v)
        print(MI_v_u)
        print(env.sym[0].price_multiplier)
        print(env.sym[1].price_multiplier)

        order1 = get_open_orders(env.sym[0])
        order2 = get_open_orders(env.sym[1])
        print(order1)
        print(order2)
        if order1 != [] and order2 != []:
            print("Amount:", order1[0]["amount"])
            print("Amount:", order2[0]["amount"])
                
    
    record(P1=data.current(env.sym[0], 'price'))
    record(P2=data.current(env.sym[1], 'price'))


    env.day_count+=1

    
    pass




# Fire off backtest

start = pd.Timestamp('2000-11-18', tz='utc')
end = pd.Timestamp('2021-1-4', tz='utc')

result = run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize,handle_data=handle_data, # Define startup function
    capital_base=100000, # Set initial capital
    data_frequency = 'daily',  # Set data frequency
    bundle='daily-bundle' ) # Select bundle

# result.to_pickle("test.pkl")

    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 100
    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark 
    #zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 



    #zipline run -f main.py -o test7.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 10000 > output.txt
    # scp -r -i algot.pem ~/Documents/Github/algot_test ubuntu@ec2-18-163-214-189.ap-east-1.compute.amazonaws.com:


# ssh -i ~/Downloads/algot.pem ubuntu@ec2-18-162-232-172.ap-east-1.compute.amazonaws.com
