class logger:
    def __init__ (self):
        pass
    
    def log(self , context, other_logs = {}):
        
        logs ={}
        logs["datetime"] = str(context.get_datetime())
       
        # add portfolio related things
        logs['portfolio value'] = context.portfolio.portfolio_value
        logs['portfolio pnl'] = context.portfolio.pnl
        logs['portfolio return'] = context.portfolio.returns
        logs['portfolio cash'] = context.portfolio.cash
        logs['portfolio capital used'] = context.portfolio.capital_used
        logs['portfolio positions exposure'] = context.portfolio.positions_exposure
        logs['portfolio positions value'] = context.portfolio.positions_value
        logs['number of orders'] = len(context.blotter.orders)
        logs['number of open orders'] = len(context.blotter.open_orders)
        logs['number of open positions'] = len(context.portfolio.positions)

        # add recorded variables from `zipline.algorithm.record` method
        for name, value in context.recorded_vars.items():
            logs[name] = value
        
        for name, value in other_logs.items():
            logs[name] = value
        
        self.print_log(logs)

    def print_log(self ,logs ):
        print("000"+str(logs))

        pass
    pass