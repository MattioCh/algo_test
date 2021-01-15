
import numpy as np
import operator

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


def misprice_index(family, u, v, tau):
    # calculates the conditional probability of u given v
    if family == 'clayton':
        U = u[-2:]
        V = v[-2:]
        theta = 2 * tau / (1 - tau)
        cuv = (V ** (-theta - 1)) * (U ** (-theta) + V ** (-theta) - 1) ** (-1 / theta - 1) 

        return cuv
    
    elif family == 'gumbel':
        U = u[-2:]
        V = v[-2:]
        theta = 1 / (1 - tau)
        A = (-np.log(U)) ** theta + (-np.log(V)) ** theta
        C = np.exp(-A ** (1 / theta))
        # pdf = c * (U * V) ** (-1) * (A ** (-2 + 2 / theta)) * ((np.log(U) * np.log(V)) ** (theta - 1)) * (1 + (theta - 1) * A ** (-1 / theta))
        cuv = C * (((- np.log(U))**theta + (-np.log(V))**theta) ** ((1-theta)/theta)) * (-np.log(V))**(theta-1) / V
    # misprice index of y given x = cvu   
        return cuv


def compare_array_with_float(arr, int_, relate):
    ops = {'>': operator.gt,
           '<': operator.lt}
    foo = True
    for i in arr:
        if not ops[relate](i,int_):
            foo = False
    return foo
        

