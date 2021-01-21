## Questions
1. When retraining, should we take the bar_counts for training_period (3500) or context.time instead (i.e. training from the beginning of time)
2. Should the frequency of training be equals to the window used to train?
3. Scaling done in periods 

## Possible Modifications
1. Tuneable parameters are placed at the top
2. Frequency of training 

## Version History
lstm.py: 
- LSTM model trained with price data 
- Trading logic based on difference with last prediction and current prediction - a very stupid way to trade
- Build subsequent models on this 
