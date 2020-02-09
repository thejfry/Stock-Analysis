import datetime
import pandas as pd
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go


class Ticker:
    def __init__(self, name):
        self.name = name
        self.data = pd.DataFrame()

    def trim_columns(self):
        for col in self.data.columns:
            if 'Unnamed' in col:
                self.data.drop(columns=col, inplace=True)

    def reformat_date(self):
        self.data['Date'] = self.data['Date'].apply(
            lambda date: datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S').date())
        self.data.set_index('Date', inplace=True)

    def load_data(self):
        self.data = pd.read_csv('./backtesting_data/finance backtesting data - ' + self.name + '.csv')
        self.trim_columns()
        self.reformat_date()

    def sma_strategy(self, means, startDate, endDate):
        for m in means:
            self.compute_sma(m)
        self.plot_strategy('SMA', startDate, endDate)

    def compute_sma(self, length):
        self.data['SMA ' + str(length)] = self.data['Close'].rolling(window=length).mean()

    def mr_strategy(self, startDate, endDate):
        self.compute_mr(15)
        self.plot_strategy('MR', startDate, endDate)

    def compute_mr(self, length):
        self.data['MR mean'] = self.data['Close'].rolling(window=length).mean()
        self.data['MR plus'] = self.data['MR mean'] + self.data['Close'].rolling(window=length).std()*2
        self.data['MR minus'] = self.data['MR mean'] - self.data['Close'].rolling(window=length).std()*2

    def plot_strategy(self, strategy, startDate, endDate):
        plot_cols = ['Close']
        for col in self.data.columns:
            if strategy in col:
                plot_cols.append(col)
        self.show_plot(strategy, plot_cols , startDate, endDate)

    def show_plot(self, strategy, plot_cols, startDate, endDate):
        py.plot([{
            'x': self.data[startDate:endDate].index,
            'y': self.data[col],
            'name': col,
        } for col in plot_cols], filename="./plots/" + self.name + '_' + strategy + '_plot.html')
