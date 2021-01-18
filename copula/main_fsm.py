
import enum
import operator
import logbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from copulas.bivariate import Bivariate
from scipy.stats import kendalltau, linregress
from statsmodels.distributions.empirical_distribution import ECDF
from transitions import Machine
from zipline import run_algorithm
from zipline.api import *
from zipline.finance import commission, slippage

from fsm_states import s
from helper import compare_array_with_float, find_Return
import math
import sys

from tensorboard import TensorBoard

# zipline_logging = logbook.NestedSetup([
#     logbook.NullHandler(level=logbook.DEBUG, bubble=True),
#     logbook.StreamHandler(sys.stdout, level=logbook.INFO),
#     logbook.StreamHandler(sys.stderr, level=logbook.ERROR),
# ])
# zipline_logging.push_application()



# class s(enum.Enum): #States
#     DEFAULT         = 0
#     L0S1            = 1  #Long sym[0] short sym[1]
#     L1S0            = 2  #Long sym[1] short sym[0]   
#     pass

# '''             Trigger             Prev State          Next State'''

# transitions_ = [["initiate",        s.DEFAULT ,         s.DEFAULT],
#                 ["order_0",         "*",                  s.L0S1],
#                 ["release",         s.L0S1,             s.DEFAULT],
#                 ["order_1",         "*",                  s.L1S0],
#                 ["release",         s.L1S0,             s.DEFAULT]
#                                                                             ]

def initialize(env):
    # set_max_leverage(3.3)
    set_benchmark(False)
    env.capital_base = 100000
    env.sym = [symbol("HQL"),symbol("HQH")]
    env.day_count = 0
    env.floor_CL = 0.2
    env.cap_CL = 0.8
    env.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    env.set_slippage(slippage.VolumeShareSlippage())
    env.leverage_flag = 0
    env.model = ""
    env.long_short_percentage = 1
    env.control =0
    env.m = Machine(states=s, transitions=transitions_,initial=s.DEFAULT)

    
    env.tensorboard = TensorBoard(log_dir= "/Users/matthewchuang/Documents/GitHub/algo_test/copula/test")
    pass


# def trade_fsm(env, data , m):
#     state = m.state
#     if state == s.INITIATE:
#         m.proceed()
#         return

#     if state == s.FIRST_1000_DAYS:
#         env.day_count += 1
#         m.exit()
#         return

#     if state == s.PROCESS_DATA:


#     return 0


def handle_data(env, data):

    if env.day_count < 1001:
        env.day_count +=1
        return

    #process data
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

    # copula
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

    MI_u_v = env.model.partial_derivative(u_v_stack)
    MI_v_u = env.model.partial_derivative(v_u_stack)


    #fsm to check order state 
    #env.control = blah


    if env.control == 0:
        print("DEFAULT")
        if sum(i < env.floor_CL for i in MI_u_v ) > 1 and sum(i > env.cap_CL for i in MI_v_u ) > 1 :
            #long u short v
            long_pos = order_target_percent(env.sym[0], env.long_short_percentage)
            short_pos = order_target_percent(env.sym[1], -env.long_short_percentage )
            env.control = 1
            
            print(-116)

            # Placing orders: if short is relatively underpriced, sell the pair
        elif sum(i > env.cap_CL for i in MI_u_v ) > 1 and sum(i < env.floor_CL for i in MI_v_u ) > 1:
            #short u long v
            long_pos = order_target_percent(env.sym[1], env.long_short_percentage )
            short_pos = order_target_percent(env.sym[0], -env.long_short_percentage )
            env.control = 2
            
            print(-123)
        
        pass

    elif env.control == 1:
        print("LOS1")
        if sum(i > env.cap_CL for i in MI_u_v ) > 1 and sum(i < env.floor_CL for i in MI_v_u ) > 1:
            long_pos = order_target_percent(env.sym[0], env.long_short_percentage)
            short_pos = order_target_percent(env.sym[1], -env.long_short_percentage )
            env.control = 2

            print(-116)
        elif sum(k > 0.2 for k in MI_u_v) > 1  and sum(k < 0.8 for k in MI_v_u) > 1:
            short_pos = order_target(env.sym[1], 0)
            long_pos = order_target(env.sym[0], 0)
            env.control = 0


    elif env.control == 2:
        print("L1S0")
        if sum(i < env.floor_CL for i in MI_u_v ) > 1 and sum(i > env.cap_CL for i in MI_v_u ) > 1 :
            #short u long v
            long_pos = order_target_percent(env.sym[1], env.long_short_percentage )
            short_pos = order_target_percent(env.sym[0], -env.long_short_percentage )
            env.control = 1

            print(-123)
        elif sum(k < 0.8 for k in MI_u_v) > 1  and sum(k >0.2 for k in MI_v_u) > 1:
            short_pos = order_target(env.sym[1], 0)
            long_pos = order_target(env.sym[0], 0)
            env.control = 0



    #loggeresss

    print("P1: ",df.iloc[-1,0])
    print("P2: ",df.iloc[-1,1])
    print("PNL: ", env.portfolio.pnl)

    print("MI_u_v:",MI_u_v)
    print("MI_v_u:",MI_v_u)


    order1 = get_open_orders(env.sym[0])
    order2 = get_open_orders(env.sym[1])
    print(order1)
    print(order2)
    if order1 != [] and order2 != []:
        print("Amount:", order1[0]["amount"])
        print("Amount:", order2[0]["amount"])
    env.tensorboard.log_algo(env)
    pass




# Fire off backtest

start = pd.Timestamp('2012-11-18', tz='utc')
end = pd.Timestamp('2021-1-4', tz='utc')

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


# ssh -i ~/Downloads/algot.pem ubuntu@ec2-18-162-232-172.ap-east-1.compute.amazonaws.com
