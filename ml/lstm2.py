import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import keras
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential # neural network
from keras.layers import Dense # final output 
from keras.layers import LSTM
from keras.layers import Dropout # prevent overfitting 

from zipline.api import record, symbol, order_target_percent, set_max_leverage
from zipline import run_algorithm
from zipline.finance import commission

# parameters 
window = 30 # length of window
training_period = 3500 # we have 5000+ trading days
selected_stock = 'AAPL'
n_stocks_to_buy = 1
optimizer = 'adam'
loss = 'mean_squared_error'
units = 50
dropout_value = 0.2
num_epoch = 10
batch_size = 32

def initialize(context):
    context.time = 0
    context.asset = symbol(selected_stock)
    context.set_commission(commission.PerShare(cost=0.001, min_trade_cost=0))

    # initialize model 
    model = Sequential()

    model.add(LSTM(units = units, return_sequences = True, input_shape = (window, 1)))
    model.add(Dropout(dropout_value))

    model.add(LSTM(units = units, return_sequences = True))
    model.add(Dropout(dropout_value))

    model.add(LSTM(units = units, return_sequences = True))
    model.add(Dropout(dropout_value))

    model.add(LSTM(units = units)
    model.add(Dropout(dropout_value))

    model.add(Dense(units = 1))

    model.compile(optimizer = optimizer, loss = loss)

    context.model = model

def handle_data(context, data):
    context.time += 1
    if context.time < training_period:
        return
    
    # training every 30 days 
    if ((context.time - training_period) % 30) == 0:
        # getting the log returns 
        price_history = np.array(data.history(context.asset, fields = "price", bar_count = training_period, frequency = "1d"))
        df = pd.DataFrame(data = price_history, columns = ['price'])
        df['return'] = np.log(df['price'] / df['price'].shift(1))
        ret = df['return'].dropna(inplace=True)
        sc = MinMaxScaler(feature_range=(0, 1))
        scaled_data = sc.fit_transform(ret)

        # get training data into right shape for input 
        X_train = []
        y_train = []
        for i in range(window, len(data)):
            X_train.append(scaled_data[i - window: i, 0])
            y_train.append(scaled_data[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)

        X_train = np.reshape(X_train, (X_train.shape[0], window, 1))

        # fitting the model
        context.model.fit(X_train, y_train, epochs = num_epoch, batch_size = batch_size)
    
    # using the model to trade 
    # reshape test_data but do not scale it 
    test_price = np.array(data.history(context.asset, fields = 'price', bar_count = window + 1, frequency = '1d'))
    test_ret = np.log()
    test_data = np.reshape(test_data, (test_data.shape[0], window, 1))

    pred = 

def analyze(context, perf):
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16,9])

    perf.portfolio_value.plot(ax=ax[0])
    ax[0].set_ylabel('portfolio value in $')

    perf['price'].plot(ax=ax[1])
    ax[1].set_ylabel('price in $')

    perf.returns.plot(ax=ax[2])
    ax[2].set_ylabel('daily returns')

    plt.legend()
    plt.show()
 
start = pd.Timestamp('2000-11-18', tz='utc')
end = pd.Timestamp('2021-1-4', tz='utc')

result = run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize,
    handle_data=handle_data, # Define startup function
    capital_base=100, # Set initial capital
    data_frequency = 'daily',  # Set data frequency
    bundle='custom-bundle2' # Select bundle
) 

result.to_pickle("test1.pkl")

'''
- closing positions
- more logic for combinations of long, short etc
- train everyday?
- train every 30 days?
- different lag
- different models in Logistic Regression
'''
# zipline run -f logreg.py -o test.csv -s 2000-11-18 -e 2021-1-4 -b custom-bundle2 --no-benchmark --capital-base 100