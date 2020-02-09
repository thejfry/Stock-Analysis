import datetime
import pandas as pd
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go
from Ticker import Ticker

cf.go_offline()


def main():
    # set date boundaries for plot
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date(2016, 1, 1)

    # Specify tickers to analyze
    tickers = ['SPY']

    for t in tickers:
        # # Collect ticker data
        current_tick = Ticker(t)
        current_tick.load_data()

        # # assess simple moving average strategy
        means = [8, 25, 55]
        current_tick.sma_strategy(means, startDate, endDate)

        # # assess mean reversion strategy
        current_tick.mr_strategy(startDate, endDate)


if __name__ == "__main__":
    print('program start\n')
    main()
    print('program done')
