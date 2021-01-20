import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from streamlit.script_request_queue import RerunData
from streamlit.script_runner import RerunException
from streamlit.server.server import Server
import streamlit.report_thread as ReportThread

def load_data(nrows):
    data = pd.read_csv("ZTR.csv", nrows=nrows)
    return data

def animate(i):  # update the y values (every 1000ms)
    #line.set_ydata(np.random.randint(0, max_rand, max_x))
    the_plot.pyplot(plt)

def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

df = pd.read_csv("ZTR.csv")
idx = df.index.size

df = load_data(idx)
df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={'date':'index'}).set_index('index')
st.line_chart(df.close)
st.line_chart(df.volume)
time.sleep(8.0) # time interval to rerun
rerun()

# day = 0
# dayIncrease = 1000
# timeUpdate = 5.0

# while(day < idx):
#     day = day + dayIncrease
#     df2 = load_data(day)
#     df2['date'] = pd.to_datetime(df2['date'])
#     df2 = df2.rename(columns={'date':'index'}).set_index('index')
#     st.line_chart(df2.close)
#     st.line_chart(df2.volume)
#     time.sleep(timeUpdate)

# rerun()