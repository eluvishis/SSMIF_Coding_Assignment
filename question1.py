""" 
program: question1_SSMIF.py
author: Eden Luvishis

This file works calculates several different parameters of stock data. First, 
it can calculate daily returns based on Adjusted Close prices of a stock. 

It then uses daily returns to calculate the Monthly Value at Risk. In order to do 
this, I sorted the returns and proceeded to find the bottom 5% of data (or other
value depending on the confidence level given). I then took the value that divided 
the top 95% from the bottom 5% by using the index of the for the given data set. 
Finally, I adjusted for time, since the daily returns do not directly correlate to
Monthly VaR. 

For Monthly Conditional VaR, I used a similar strategy. I isolated the
lowest 5% (or other depending on confidence level), and found the average of this
new list. This allowed me to find the average "tail risk" associated with the stock. 
Again, I adjusted for time. 

For the last part, I used the sample standard deviation (SSD) as a measure of volatility
because the SSD shows how dispersed returns are for a given stock. I used sample SD 
instead of populuation SD because the year worth of data that I am downloading, only 
represents a sample of the stock's total data. Therefore, the sample SD would more
closely demonstrate the stocks actual volatility.

""" 


import pandas as pd
import pandas_datareader as web
import datetime as dt
import statistics as s
import math as m


#Part 1

def Daily_Returns(df):
    """Returns a list of daily returns as percentages. Accepts Dataframe as argument """

    #creates a list of daily returns
    returns = []
    for i in range(len(df['Adj Close'])):
        #on first day, there is no return
        if i == 0:
            returns.append(0)
        else:
            num = ((df['Adj Close'][i]/df['Adj Close'][i-1]) - 1) * 100 #formula for return %
            returns.append(round(num, 4))
            
    return returns


#Part 2

def Monthly_VaR(ticker, confLev = 0.05):
    """Returns Monthly Value at Risk (%) for a Ticker and Confidence Level"""

    #download data from Yahoo finance
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 12, 31)
    stock = web.DataReader(ticker, 'yahoo', start, end) 

    #call Daily_Returns function for specific stock
    dailyreturns = sorted(Daily_Returns(stock))

    #calculate cutoff point
    cutoff = len(dailyreturns) * confLev
    cutoff = round(cutoff)

    #extract the VaR from returns based on confidence
    VaR = dailyreturns[cutoff]

    #adjust for time (20 trading days)
    monret = VaR * m.sqrt(20)

    return monret

#Part 3

def Monthly_CVaR(ticker, confLev = 0.05):
    """Returns Monthly Conditional Value at Risk (%) given ticker and Confidence Level""" 

    #download data from yahoo finance
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 12, 31)
    stock= web.DataReader(ticker, 'yahoo', start, end) 

    #call Daily_Returns function for specific stock
    dailyreturns = sorted(Daily_Returns(stock))

    #calculate cutoff point for confidence level 
    cutoff = round(len(dailyreturns) * confLev)
    tail = dailyreturns[:cutoff] 
    avgtail= s.mean(tail) #get average for the "worst" returns

    #adjust for time (trading month is 20 days)
    monCVaR = avgtail * m.sqrt(20) 

    return monCVaR

#Part 4

def Monthly_Volatility(ticker):
    """Returns Monthly Volatility as adjusted Standard Deviation"""

    #download stock data from yahoo finance
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 12, 31)
    stock = web.DataReader(ticker, 'yahoo', start, end) 

    #call Daily_Returns function for specific stock
    dailyreturns = Daily_Returns(stock)

    #sample standard deviation
    vol = s.stdev(dailyreturns) 

    #adjusted for 20 trading days/month
    monVol = vol * m.sqrt(20) 

    return monVol



#Testing

print(Monthly_VaR("AAPL"))

print(Monthly_CVaR("AAPL"))

print(Monthly_Volatility("AAPL"))



 
 