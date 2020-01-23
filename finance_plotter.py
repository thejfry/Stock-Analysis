import datetime
import pandas as pd
import plotly.offline as py
import cufflinks as cf

cf.go_offline()

def main():
    # Set date boundaries for plot
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date(2016, 1, 1)

    # Read in data from csv file
    SPY = pd.read_csv('finance backtesting data - SPY.csv')

    # Reformat date column and set it as index
    SPY['Date'] = SPY['Date'].apply(lambda date: datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S').date())
    SPY['Date'] = pd.to_datetime(SPY['Date'])
    SPY.set_index('Date', inplace=True)

    # Drop unnecessary columns from data
    for c in SPY.columns:
        if 'Unnamed' in c:
            SPY = SPY.drop(columns=c)

    # Compute moving averages on closing price
    means = [8, 25, 55]

    SPY_means = pd.DataFrame(index=SPY.index)
    SPY_means['Close'] = SPY['Close']
    for m in means:
        SPY_means['SMA ' + str(m)] = SPY_means['Close'].rolling(window=m).mean()

    # Plot Closing prices
    py.plot([{
        'x': SPY_means[startDate:endDate].index,
        'y': SPY_means[col],
        'name': col
    } for col in SPY_means.columns], filename='stock_plotter.html')


if __name__ == "__main__":
    print('program start\n')
    main()
    print('program done')
