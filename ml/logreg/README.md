## File description for logistic regression
1. logreg.py: 
    - original code 
    - training once after training_period
    - simple logic, no closing positions - only shorting when trend downwards

2. logreg2.py:
    - training every 30 days after training_period
    - simple logic, no closing positions

3. logreg3.py:
    - add trading logic for moving averages and closing positions

### Todo:
- use volume data to identify high volume days for exit signals 
- fine tune parameters, e.g. number of lags, SMA to EMA, ...
- predict further ahead, e.g. market movement in the next 30 days instead of just one step ahead
- scale data for optimal performance?

### Observations (with sample size of 3 tickers):
1. More conservative:
    - using exit signals with simple moving averages 
2. More accurate predictions when retraining every 30 days 