
import enum
import operator

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


class s(enum.Enum): #States
    Error           = 0
    INITIATE        = 1
    FIRST_1000_DAYS = 2
    PROCESS_DATA    = 3
    MAKE_ORDER      = 4
    EXCEED_LEVERAGE = 5
    PRINT_LOG       = 6
    EXIT_FSM        = 7

    pass

'''             Trigger             Prev State          Next State'''

transitions_ = [["initiate",        s.INITIATE ,        s.FIRST_1000_DAYS],
                ["proceed",         s.FIRST_1000_DAYS,  s.PROCESS_DATA],
                ["proceed",         s.PROCESS_DATA,     s.MAKE_ORDER],
                ["proceed",         s.MAKE_ORDER,       s.PRINT_LOG],
                ["exceed_leverage", s.MAKE_ORDER,       s.EXCEED_LEVERAGE],
                ["proceed",         s.EXCEED_LEVERAGE,  s.PRINT_LOG],
                ["print_log",       s.PRINT_LOG,        s.EXIT_FSM],
                ["exit",            s.EXIT_FSM,         s.EXIT_FSM]
                                                                            ]

def initialize(env):
    # set_max_leverage(3.3)
    set_benchmark(False)
    env.capital_base = 100000
    env.sym = [symbol("NSC"),symbol("CSX")]
    env.day_count = 0
    env.floor_CL = 0.05
    env.cap_CL = 0.85
    env.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    env.set_slippage(slippage.VolumeShareSlippage())
    env.leverage_flag = 0
    env.model = ""
    env.long_short_percentage = 1
    env.m = Machine(states=s, transitions=transitions_,initial=s.INITIATE)
    pass


def trade_fsm(env, data , state , m ):
    
    if state == s.INITIATE:
        m.proceed()
        return

    if state == s.FIRST_1000_DAYS:


    return


def handle_data(env, data):

    while env.m.state != s.EXIT_FSM:
        trade_fsm(env , data, env.m.state , env.m)
        pass

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

result.to_pickle("test.pkl")


#zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 100
#zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark 
#zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 



#zipline run -f main.py -o test7.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle --no-benchmark --capital-base 10000 > output.txt
# scp -r -i algot.pem ~/Documents/Github/algot_test ubuntu@ec2-18-163-214-189.ap-east-1.compute.amazonaws.com:


# ssh -i ~/Downloads/algot.pem ubuntu@ec2-18-162-232-172.ap-east-1.compute.amazonaws.com
