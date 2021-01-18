
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
        
def put_into_bin(arr , w):
    catagory = []
    length = max(arr) - min(arr)
    num_of_bin = int((length/w))+1
    rem = length - (num_of_bin-2) * w 
    rem = rem/2
    min_ = min(arr)
    catagory.append(min_)
    catagory.append(min_+ rem)
    for i in range(2,num_of_bin-1):
        catagory.append(min_ + i * w)
    bin_indices = np.digitize(arr, catagory)
    return bin_indices , catagory






    
