from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading, Asset
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Choose ticker symbols of interest. 
        # For example, choosing a well-known company with frequent trading activities.
        self.tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Use daily data for our analysis
        return "1day"

    @property
    def assets(self):
        # The assets we're interested in trading
        return self.tickers

    @property
    def data(self):
        # Define the data we want to analyze
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            try:
                # Compute the simple moving average (SMA) for trading volume over the last 10 and 30 days
                sma_short = ta.sma(pd.Series([i[ticker]["volume"] for i in data["ohlcv"]]), length=10).iloc[-1]
                sma_long = ta.sma(pd.Series([i[ticker]["volume"] for i in data["ohlcv"]]), length=30).iloc[-1]
                
                # If recent volume (SMA10) significantly exceeds average volume (SMA30), it might indicate
                # increased interest or activity that could be revenue-related or impactful to the market price.
                if sma_short > sma_long * 1.5:  # For example, an arbitrary threshold of 50% increase
                    allocation_dict[ticker] = 1.0 / len(self.tickers)  # Allocate evenly between tickers meeting criteria
                else:
                    allocation_dict[ticker] = 0  # Do not allocate to this ticker
            except IndexError:
                # In case there are not enough points to calculate SMA
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)