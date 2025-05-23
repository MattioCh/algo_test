
import numpy as np
import operator

def find_Return(price):
    ret = (price - price.shift(1))/price
    ret = ret.drop(ret.index[0])
    # fill the nan values with 0
    ret = ret.fillna(value = 0)
    return ret 

def compare_array_with_float(arr, int_, relate):
    ops = {'>': operator.gt,
           '<': operator.lt}
    foo = True
    for i in arr:
        if not ops[relate](i,int_):
            foo = False
    return foo
        


