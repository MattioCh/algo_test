# algo_test
## Goal
- On 31/Jan, Achieve 10% CAGR on any mean reversion or momentum strategy
  - Possible strategy
    - Copula pair trading with cluster and more stats test
    - Reimplementation on the US Equity statistical arbitrage model with clustering
    - Price prediction with more classical pricing theories and macro data (possibly machine learning, need to learn more tensorflow)
      - https://github.com/tensorflow/probability/tree/master/tensorflow_probability/examples/jupyter_notebooks
   
## 2/Jan:
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
  - https://www.youtube.com/watch?v=N2KIm1it1HQ&t=946s&ab_channel=ErolAspromatis
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
    - https://www.linkedin.com/pulse/how-much-money-would-cost-setup-high-frequency-trading-ariel-silahian/

  
  
  
