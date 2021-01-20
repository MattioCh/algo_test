# algo_test

## Todo

- Optimise copula with more stocks at the same time
- **multithreading** for cross testing different sets of tickers and different set of parameter (for improving specific strategy)
- make the program more like FSM
- possibly use qt to wrap the program as a simulator
- find more people?
- find professor to help us?
- Test report matplotlib function to instantly show the performance
- Find more minute data
- visualisation, output.txt ->> do in time visualisation 2000 ,2001  

##momentum

##mean reversion 
## Goal

- On 31/Jan, Achieve 10% CAGR on any mean reversion or momentum strategy
  - Possible strategy
    - Copula pair trading with cluster and more stats test
    - Reimplementation on the US Equity statistical arbitrage model with clustering
    - Price prediction with more classical pricing theories and macro data (possibly machine learning, need to learn more tensorflow)
      - <https://github.com/tensorflow/probability/tree/master/tensorflow_probability/examples/jupyter_notebooks>



## 2/Jan

- algogene runtime is too long
  - difficult to operate and research strategy
  - cannot fetch all the data to try out in Jupyter
- backtrader (python module) is a possible choice
  - can linked to interactive broker straight away
  - language is messy though it is frequently maintained
- zipline is still possibly the best
  - maintained by quantopian, used to be the largest backtesting website
  - problem: difficult to stream data
- Quantconnect:
  - great resources but costly, take time to run
  - can paper trade

## 3/Jan

- Testing out Zipline
  - Have to run on python 3.6
  - conda create -n "your-name" python=3.6
  - conda activate, blah, blah, blah..
  - ipython kernel install --name "the name you want" --user
  - still haven't figured out how to source bundle easily
  - try downloading all the stock data from yahoo finance
    - fail, too low RAM on laptop
    - tried on google collab crash again
    - dont' use this list of stock name from this page "https://investexcel.net/all-yahoo-finance-stock-tickers/"
  - major problem today:
    - too many stock exchange, don't know what data to target
      - many companies are very small, and they are still listed, but have ZERO value
      - These companies are most prevalent in PKL(Pink Sheet) not publicly listed on stock exchange
    - tried quantconnect to scrap largest trading volume stock but the coarse universe doesn't allow scarping down name
    - better way -> best scenario is to find the UNION of data of IBKR and Yahoo finance

## 4/Jan

- Find out a script to fix data bundle problem
  - https://github.com/aspromatis/zipline_bundle
  - <https://www.youtube.com/watch?v=N2KIm1it1HQ&t=946s&ab_channel=ErolAspromatis>
  - need to seperate each stock as each file
  - Todo
    - setup data bundle
    - script for downloading most of the stock into a file
- Some research on HFT
  - FPGA is a common hardware standard for fast computing speed
  - HVDL is the underlying language
  - pynq is a FPGA hardware that allows to write logic gates in Jupyter notebook.
    - according this paper https://arxiv.org/pdf/1705.05209.pdf, the inference speed is 3x faster than normal python OpenCV library
    - inference speed is 30x faster than the C version in single thread
    - cost roughly 1000hkd if buy in TW, don't buy in xilinx official website cuz it's 600hkd more expensive.
    - can use tensorflow website
    - not sure if it can use interactive broker api
      - can be difficult to configure the client server if extra library is needed
  - HFT setup is expensive
    - <https://www.linkedin.com/pulse/how-much-money-would-cost-setup-high-frequency-trading-ariel-silahian/>

## 5/Jan

- Registering bundle on zipline if you do not have .zipline (for window)
  1. git clone <https://github.com/aspromatis/zipline_bundle> - somewhere in your computer
  2. copy everything in extension.py from the repo above
  3. find Users\<your name>\anaconda3\envs\env_zipline\Scripts\zipline-script.py (main thing is find zipline-script.py
  4. paste the code from extension.py in the if statement that starts with (if __name__ == "__main__": ...) above the original expressions there. The imports go at the top of the file.
  5. change the path in csvdir_equities to the actual path where you cloned the repo
  6. save zipline-script.py
  7. in anaconda prompt, activate your environment, then $zipline ingest -b custom-bundle (or your bundle name)

- General guidline to use zipline bundle
  - find the .zipline file in you $USER, it is a hidden file. 
  - Paste the extension.py file in there.
  - the extension.py file also manage the startdate in the zipline bundle so you can adjust it if somedays are missing or extra day is shown in command line.
  - Also, git clone <https://github.com/aspromatis/zipline_bundle> and take the csvdir.py and paste it into your zipline/data/bundles and replace the one inside.

  - Lastly, run $zipline ingest -b custom-bundle
- Problem today:
  - Need to setup for knowlten, possibly use linux and ssh with vscode so it still have a proper workspace

  - Now the data can be easily download, and there is a script in the data file to write new data everyday.

  - However, every stocks start different day. I tried to download all the stocks from 2000/1/29, however, stocks like TSLA only have data starting from 2010

  - Solution:
  
    - Put 0 Value for all of the previous stock

    - Register different bundles, where some bundle indlucde stokcs that are longer than 10 years, but some don't.

    - This may effect the clustering process tho... due to difference in data dimension.

## 6/Jan

- improve the clustering process with 1500 stocks data spanning twenty years
  - compile a merge.pkl file that contains all the stock that have full history, however some stocks are excluded because it might starts having value in later time (ex. TSLA)
  - Might need to set 0 for previous value since 0 value means they don't exist yet and this can give a better overall dataset.
- minutes data work
  - however only 30 days with 2minutes data is provided by finance
  - even though yfinance let you set parameter for 60 days, the data actually only starts at 30 days.

##8/Jan
- add data_clean.py to clean up tickers that have the wrong shape
  - have a stable version for the datas folder and it can be used most of the time.
- Added the Misprice index for different copulas and added the trading logic
  
## 11/Jan
- fixed the copula trading logic, the output is not between [0,1] and it needs to apply an inverse function
- added the leverage logic so that the leverage goes into infinity and keep buying

##12/Jan
- increase the window to check Misprice index
  - This makes the trading algorithm more conserve and it will only perform long short and the misprice signel is generated for 2 consecutive days.
## 13/Jan On the way to going crazy

- AWS is better than Azure because Azure would start charging you money starting from the third month
- future plan on cloud computing:
  - need to research more about how much faster it is to use a more expensive cpu
  - possibly try the cpu with Steven because he recently got a better desktop

## 14/Jan python imports....
- took too much time on figuring how to imports, here are some rules:
  - if you have a helper.py in the same directory as your main.py, you will import the function **ONE BY ONE** as follows:
  - ```python
    from helper import func1, func2, func3
    ```
  - if you have a folder call foo and there is a file called helper.py that you want to use, then you have to make sure you have another file that is called __init__.py to make sure python knows the **foo** is a directory. You can import with the following code
  - ```python
    from foo.helper import func1, func2, func3
    ```
  - so let's stop using our time solving imports


## 16/Jan 
- implemented the trading logic with a few modules:
  - transitions: basically a python module that has a very good FSM structure that and you can also use Enums. The speed doesn't slow down by too much
- Distance method is trash. The problem is the distance between stocks changes drastically over the time. Therefore, the exit threshold changes to a margin where the initial trading positiion is no longer favourable. Even if you fixed the initial trading signal, this is actually worse because if the initial mean spread is too high, then you trade can never exit. 
- find some seniors amazing work https://github.com/wywongbd/pairstrade-fyp-2019 
  - should ask and cold email about the project

## 17/Jan
-(Magd you should write this)
-simple Ml with logictic regression. Exceptional result with a good stock, however, the results is very stock dependent, can't really say how it's going to predict if the price might go down.

##18/Jan
- Added the Tensorboard thing
  - very useful for tracking the progress **in real time**
  - can add more graph to monitor but Xian can use streamlit in the futrue so why bother tnesorboard anymore?
- tried a new method --> probabilitic markov chain model
  - I guess it's a very very simple version of RL because it doesn't look at the action space, and only look at the current state and calculates the probability of the expected value of next day's price. I used the Scott's rule to seperate the bin number but then maybe I can do it dynamically??
  - The result is good:
    - shapre: 0.8 (lowest at 0.4), return 35 for in 14 years, 28& per year. However, the max drawdown is 50% in 2019, but return is 200% in 2020. So, who knows? (haven't batch tested on more stocks, only on AAPL for now, though it out performs it so maybe it's good?)
  - Urgently need Batch testing method

## 19/Jan
- Help Xian to setup for zipline..
  - The process is still way to long... maybe need to write a bash script to streamline the process?
- Xian made the streamlit real-time work!!!
  - let's call it stream-realtime, happy:)
  - However, he haven't pushed yet, so don't know how to output yet.
  - Tbh, it's possible to use jupyter notebook I just realised, but jupyter notebook might be bad for streaming in real-time and there is less flexibility... tbh... this is my bad decision
- Need to find more software work. Again tbh, I think it's better to let Xian learn the trading logic? But, I feel like if not in person, it feels harder to explain the trading logic and some simple ideas..
- Training frequency needs to increase for ML, sharpe is significanlty higher and I guess it just make the decision more "informed" and conservative. might to use validation to see whether there is overfitting.

##20/Jan
- Setup some basic stuff for pyqt
  - I (matthew) can't download the Qt designer, whyyyyy????? Some people in the forum also said they couldn't download because the server is down. But... how does Xian downloaded it...
  - Need a better design and more detail object name in the design to make future work process easier
  - For one point, I thought we need to use a webhost to verify new accounts. Now I realised, it's possible to encrypt the time that they can use,also the date they start as the key, and anytime after this, then they cannot use the software anymore, I mean I don't really know why I am so protective about this thing... maybe I should really change my perspective about protecting IP and releasing it to more people. I truly want more people to use it, but I am just scared that people would just join us(if they will ofc...), and just leave with the software... sad... Maybe I am thinking about this wrongly...
- magd is downloadiing the keras, maybe she needs to log the problem of how to successfully download keras with the zipline env.
- I think the next few things we need urgently is the minute data and a more professional guidance.