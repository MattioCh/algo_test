
from zipline.api import *
from scipy.stats import kendalltau
from zipline.finance import (commission)
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from zipline.api import order_target, record, symbol
from zipline.finance import commission, slippage
from statsmodels.genmod.families import family

def find_Return(price):
    ret = (price - price.shift(1))/price
    ret = ret.drop(ret.index[0])
    # fill the nan values with 0
    ret = ret.fillna(value = 0)
    return ret

def _lpdf_copula(family, u, v,tau):

    if  family == 'clayton':
        theta = 2 * tau / (1 - tau)
        pdf = (theta + 1) * ((u ** (-theta) + v ** (-theta) - 1) ** (-2 - 1 / theta)) * (u ** (-theta - 1) * v ** (-theta - 1))

    elif family == 'gumbel':
        theta = 1 / (1 - tau)
        A = (-np.log(u)) ** theta + (-np.log(v)) ** theta
        c = np.exp(-A ** (1 / theta))
        pdf = c * (u * v) ** (-1) * (A ** (-2 + 2 / theta)) * ((np.log(u) * np.log(v)) ** (theta - 1)) * (1 + (theta - 1) * A ** (-1 / theta))
        
    return np.log(pdf)


def initialize(context):
    
    
    context.sym = [symbol('ZNH'),symbol("CEA")]
    context.day_count = 0
    context.model = ""

    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    # Skip first 300 days to get full windows
    if context.day_count < 1000:
        context.day_count +=1
        return
    if context.day_count <1001:
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
        
        context.model = "clayton" if clayton.sum() < gumbel.sum() else "gunbel"
        
        context.day_count +=1 
        return


    print(context.model)
    


    record(AAPL=data.current(context.sym, "price"))
    context.day_count += 1
    pass




#zipline run -f main.py -o test.csv -s 2000-11-18 -e 2021-1-5 -b custom-bundle --no-benchmark 
#zipline run -f main.py -o test.csv -s 2000-11-18 -o result.pkl -e 2021-1-5 -b custom-bundle --no-benchmark 
#zipline run -f main.py --data-frequency minute -o test1.csv -s 2000-11-18 -e 2021-1-5 -b minute-bundle --no-benchmark 



