
from zipline import run_algorithm
from zipline.api import *
from zipline.finance import commission, slippage

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from markovfsm import Chain
from markovfsm.plot import transitions_to_graph
from graphviz import Digraph

from tensorboard import TensorBoard
from helper import find_Return, compare_array_with_float , put_into_bin, expected_value 

def initialize(env):
    # set_max_leverage(3.3)
    set_benchmark(False)
    env.capital_base = 100000
    env.sym = symbol("MTN")
    env.day_count = 0
    env.floor_CL = 0.05
    env.cap_CL = 0.95
    env.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    env.set_slippage(slippage.VolumeShareSlippage())
    env.leverage_flag = 0
    env.model = ""
    env.long_short_percentage = 1
    env.hold_flag = 0
    env.tensorboard = TensorBoard(log_dir= "/Users/matthewchuang/Documents/GitHub/algo_test/Markov/test")
    pass



def handle_data(env, data):
    # Skip first 1000 days to get full windows
    if env.day_count < 1000:
        env.day_count +=1
        return
        # trading happens 
    else:
        df = data.history(env.sym , "close", bar_count = env.day_count, frequency = "1d")
        ret = find_Return(df)
        h = ret.std() *3.49 / len(ret)**(1/3)
        ret_list = ret.tolist()
        bins , slices = put_into_bin(ret_list, h)
        chain = Chain(max(bins)+1, bins[0])
        for i in range(1,len(bins)):
            chain.learn(bins[i])
        prob = chain.get_transitions_probs(bins[-1])
        
        pos = 0


        prob = chain.get_transitions_probs(bins[-1])
        ev = expected_value(slices, prob)
        if ev>0:
            order_target_percent(env.sym,1)
        else:
            order_target_percent(env.sym,-1)

        #print

        print("--------------------------------")
        print(df.index[-1])
        print("PNL: ", env.portfolio.pnl)
        print(ev)
        order  = get_open_orders(env.sym)
        print(order)
        if order != []:
            print("Amount:", order[0]["amount"])
        
        env.tensorboard.log_algo(env)



        record(P=data.current(env.sym,"price"))
        record(EV = ev)

        


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

result.to_pickle("test4.pkl")

    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 100
    #zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark 
    #zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 



    #zipline run -f main.py -o test7.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 10000 > output.txt
    # scp -r -i algot.pem ~/Documents/Github/algot_test ubuntu@ec2-18-163-214-189.ap-east-1.compute.amazonaws.com:


# ssh -i ~/Downloads/algot.pem ubuntu@ec2-18-162-232-172.ap-east-1.compute.amazonaws.com

#tensorboard --logdir=test/ --host localhost --port 8088