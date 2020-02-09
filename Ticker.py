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

    def compute_sma(self, length):
        self.data['SMA ' + str(length)] = self.data['Close'].rolling(window=length).mean()

    def plot_sma(self, startDate, endDate):
        plot_cols = ['Close']
        for col in self.data.columns:
            if 'SMA' in col:
                plot_cols.append(col)
        self.show_plot(startDate, endDate, plot_cols)

    def show_plot(self, startDate, endDate, plot_cols):
        py.plot([{
            'x': self.data[startDate:endDate].index,
            'y': self.data[col],
            'name': col,
        } for col in plot_cols], filename="./plots/" + self.name + '_sma_plot.html')
