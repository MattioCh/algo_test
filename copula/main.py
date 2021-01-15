
from zipline import run_algorithm
from zipline.api import *
from zipline.finance import commission, slippage
from scipy.stats import kendalltau
from scipy.stats import linregress
from zipline.finance import (commission)
from statsmodels.distributions.empirical_distribution import ECDF
import operator
from statsmodels.genmod.families import family

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append('/Users/matthewchuang/Documents/GitHub/algo_test/copula/')
from helper.helper import find_Return, _lpdf_copula,compare_array_with_float,misprice_index

def initialize(context):
    # set_max_leverage(3.3)
    set_benchmark(False)
    context.capital_base = 100000
    context.sym = [symbol("NSC"),symbol("CSX")]
    context.day_count = 0
    context.model = ""
    context.floor_CL = 0.05
    context.cap_CL = 0.85
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())
    context.leverage_flag = 0
    pass



def handle_data(context, data):
    # Skip first 1000 days to get full windows
    if context.day_count < 1000:
        context.day_count +=1
        return
    elif context.day_count > 1000 and context.day_count %500 == 1:
        df = data.history(context.sym , "close", bar_count = context.day_count, frequency = "1d")
        ret = find_Return(df)
        ret_1 = ret.iloc[:,0]
        ret_2 = ret.iloc[:,1]
        ecdf_1 = ECDF(ret_1)
        ecdf_2 = ECDF(ret_2)
        tau_ = kendalltau(ret_1,ret_2)[0]

        u = ecdf_1(ret_1)
        v = ecdf_2(ret_2)
        
        clayton = _lpdf_copula("clayton", u, v,tau_) 
        gumbel = _lpdf_copula("gumbel",u,v,tau_)
        
        context.model = "clayton" if clayton.sum() > gumbel.sum() else "gumbel"

        # trading happens 
    elif context.day_count > 1000:
        df = data.history(context.sym , "close", bar_count = context.day_count, frequency = "1d")

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
        ecdf_1 = ECDF(ret_1)
        ecdf_2 = ECDF(ret_2)
        tau_ = kendalltau(ret_1,ret_2)[0]

        u = ecdf_1(ret_1)
        v = ecdf_2(ret_2)
        # Run linear regression over history return series 
        # return desired trading signal ratio (coefficient)
        # for every sym1 that is bought/sold, coef units of sym2 is sold/bought
        
        # coef = linregress(df.iloc[-500:,:]).slope 

        # Trading logic 
        
        # Misprice index 
        MI_u_v = misprice_index(context.model, u, v, tau_)
        MI_v_u = misprice_index(context.model, v, u, tau_)

        compare_array_with_float
        # Placing orders: if long is relatively underpriced, buy the pair
        # print("P1: ",df[-1,0])
        # print("P2: ",df[-1,1])
        # print("PNL: ", context.account.pnl)
        # print(u)
        # print(v)
        # print(MI_u_v)
        # print(MI_v_u)
        if context.leverage_flag == 0:
            if compare_array_with_float(MI_u_v, context.floor_CL,"<") and compare_array_with_float(MI_v_u, context.cap_CL,">"):
                #long u short v
                long_pos = order_target_percent(context.sym[0], 0.4)
                short_pos = order_target_percent(context.sym[1], -0.4 )
                print(-116)

            # Placing orders: if short is relatively underpriced, sell the pair
            elif compare_array_with_float(MI_u_v, context.cap_CL,">") and compare_array_with_float(MI_v_u, context.floor_CL,"<"):
                #short u long v
                long_pos = order_target_percent(context.sym[1], 0.4 )
                short_pos = order_target_percent(context.sym[0], -0.4 )
                print(-123)
            else:
                short_pos = order_target(context.sym[1], 0)
                long_pos = order_target(context.sym[0], 0)
                print(-127)
            context.leverage_flag = 1 if context.account.net_leverage > 3  else 0
            pass

        else:
            if (MI_u_v[-1] > context.floor_CL and MI_v_u[-1] < context.cap_CL) or (MI_u_v[-1] > context.floor_CL and MI_v_u[-1] < context.cap_CL):
                short_pos = order_target(context.sym[1], 0)
                long_pos = order_target(context.sym[0], 0)
                context.leverage_flag = 0 if context.account.net_leverage < 3 else 1
                print(-137)
                pass
            pass
        
        print("P1: ",df.iloc[-1,0])
        print("P2: ",df.iloc[-1,1])
        print("PNL: ", context.portfolio.pnl)
        # print("coef:",coef)
        print(u)
        print(v)
        print(MI_u_v)
        print(MI_v_u)

        order1 = get_open_orders(context.sym[0])
        order2 = get_open_orders(context.sym[1])
        print(order1)
        print(order2)
        if order1 != [] and order2 != []:
            print("Amount:", order1[0]["amount"])
            print("Amount:", order2[0]["amount"])
                
    
    record(P1=data.current(context.sym[0], 'price'))
    record(P2=data.current(context.sym[1], 'price'))


    context.day_count+=1

    
    pass

start = pd.Timestamp('2000-11-18', tz='utc')
end = pd.Timestamp('2021-1-4', tz='utc')


# Fire off backtest
result = run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize,handle_data=handle_data, # Define startup function
    capital_base=100000, # Set initial capital
    data_frequency = 'daily',  # Set data frequency
    bundle='daily-bundle' ) # Select bundle

result.to_pickle("test.pkl")

    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 100
    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark 
    #zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 



    #zipline run -f main.py -o test7.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 10000 > output.txt
    # scp -r -i algot.pem ~/Documents/Github/algot_test ubuntu@ec2-18-163-214-189.ap-east-1.compute.amazonaws.com:


