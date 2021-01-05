# algo_test

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
