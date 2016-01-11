import matplotlib.pyplot as plt     # standard abbreviation
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

import numpy as np
import urllib
import datetime as dt


# left off here: https://www.youtube.com/watch?v=Blw7OF_-hXk&index=1&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter


def graph_data(stock):

    fig = plt.figure()

    # shape(one by one) starting point(0,0)
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10y/csv'

    source_code = urllib.request.urlopen(stock_price_url).read().decode()

    stock_data = []
    split_source = source_code.split('\n')

    for line in split_source:
        split_line = line.split(',')
        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)

    '''
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True)
    dateconv = np.vectorize(dt.datetime.fromtimestamp)
    date = dateconv(date)
    '''


    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          # %Y = full year. 2015
                                                          # %y = partial year. 15
                                                          # %m = number month
                                                          # %d = number day
                                                          # %H = hours
                                                          # %M = minutes
                                                          # %S = seconds
                                                          # 12-06-2014
                                                          # %m-%d-%Y
                                                          converters={0: bytespdate2num('%Y%m%d')})


    ax1.plot_date(date, closep, '-', label='Price')

    # labels
    ax1.plot([], [], linewidth=5, label='loss', color='r', alpha=0.5)
    ax1.plot([], [], label='gain', linewidth=5, color='g', alpha=0.5)
    ax1.axhline(closep[0], color='k', linewidth=5)

    # fill graphs
    ax1.fill_between(date, closep, closep[0], where=(closep > closep[0]), color='g', alpha=0.5)
    ax1.fill_between(date, closep, closep[0], where=(closep < closep[0]), color='r', alpha=0.5)
    # grabs each x-axis label and tilts it 45 deg
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    #defines the grid
    ax1.grid(True) #, color='g', linestyle='-', linewidth=5)
    # color axis labels
    ax1.xaxis.label.set_color('c')
    ax1.yaxis.label.set_color('r')
    ax1.set_yticks([0, 25, 50, 75])

    ax1.spines['left'].set_color('c')
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_linewidth(5)

    ax1.tick_params(axis='x', colors='#f06215')

    #adds title
    plt.title(stock)
    # add x and y labels
    plt.xlabel('Date')
    plt.ylabel('Price')
    # adds a legend
    plt.legend()

    # defines the subplot properties
    plt.subplots_adjust(left=0.09, bottom=0.18, right=0.94, top=0.90, wspace=0.2, hspace=0)

    # Show plot
    plt.show()

graph_data('EBAY')




