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

    for tick in tickers:
        # # Collect ticker data
        current_tick = Ticker(tick)
        current_tick.load_data()

        # # compute moving averages
        means = [8, 25, 55]
        for m in means:
            current_tick.compute_sma(m)

        # # plot closing price with moving averages
        current_tick.plot_sma(startDate, endDate)


if __name__ == "__main__":
    print('program start\n')
    main()
    print('program done')
