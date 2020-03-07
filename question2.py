"""
program: question2_SSMIF.py
author: Eden Luvishis

This file manipulates stock data downloaded from yahoo finance using Pandas_datareader. 
The file can create a SQLite3 database table and fill it with data from historical stock
metrics. 

It can then find the Monthly Value at Risk from an already existing database
by first calculating daily returns and then finding the Monthly VaR. I used the same strategy
as in Question 1 to find the Monthly VaR value: sorting all return data, and because it is
discrete, cutting off the value that lies at the edge of the confidence level desired. 

"""


import sqlite3 as sq
import datetime as dt
import pandas_datareader as web
import math as m

#Part 1

def Fill_Table(ticker):
    """Downloads stock data for ticker and saves it to SQLite3 Database Table"""

    #downloads data from yahoo using pandas_datareader
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 12, 31)
    data = web.DataReader(ticker, 'yahoo', start, end)
    data.reset_index(inplace=True)
    data.set_index("Date", inplace=True) #sets index as "Date" column


    #creates and connects DB in working directory
    sql_data = 'SSMIF.db' 
    cnct = sq.connect(sql_data) 

    #deletes existing table so function can be rerun
    cnct.execute("DROP TABLE IF EXISTS Stock_Data") 

    #creates table
    cnct.execute('''CREATE TABLE "Stock_Data" ( 
        "Timestamp" INTEGER NOT NULL, 
        "Open" DECIMAL(10,2), 
        "High" DECIMAL(10,2), 
        "Low" DECIMAL(10,2), 
        "Close" DECIMAL (10,2), 
        "Adj_Close" DECIMAL (10,2) 
        )''' )

    #iterate through DF rows and add them to SQL Table
    for i in range(len(data["Open"])):
        #retrieves index column which is a timestamp object and converts it to a date object
        date = data.index[i].date() 

        openp = data["Open"][i]
        highp =  data["High"][i]
        lowp = data["Low"][i]
        closep = data["Close"][i]
        adj = data["Adj Close"][i]

        data_tuple = (date, openp, highp, lowp, closep, adj)

        #SQL statement to insert data into table
        sqlite_insert_with_param = """INSERT INTO Stock_Data (Timestamp, Open, High, Low, Close, Adj_Close) 
                    VALUES (?,?,?,?,?,?)""" 

        cnct.execute(sqlite_insert_with_param, data_tuple)

    cnct.commit()

    cnct.close()


#Part 2

def Daily_Returns(l):
    """Returns a list of daily returns as percentages """

    returns = []
    for i in range(len(l)):
        #on first day, there is no return
        if i == 0:
            returns.append(0)
        else:
            num = ((l[i]/l[i-1]) - 1) * 100 #formula for return %
            returns.append(num)
            
    return returns


#Part 3

def Monthly_VaR(confLevel = 0.05):
    """Returns the Monthly Value at Risk (%) for a SQL Table of Historical Stock Data"""

    #connect DB
    conn = sq.connect('SSMIF.db') 
    c = conn.cursor()

    #create list of Adj Closes from DB
    l = []
    for row in c.execute('SELECT Adj_Close FROM Stock_Data'):
            l.append(row[0])

    #run Daily_Returns function to get list of returns
    dailyreturns = Daily_Returns(l)

    #sort daily returns and cutoff at confidence level
    dailyreturns = sorted(dailyreturns)
    cutoff = round(len(dailyreturns) * confLevel) #round to integer value to use as index for cutoff

    VaR = dailyreturns[cutoff] #this is the value closest to the confidence %

    #the VaR is based on daily returns so it has to be adjusted for time.
    #One month is 20 trading days
    monVaR = VaR * m.sqrt(20)

    return(monVaR)

#Testing the functions

Fill_Table("TSLA")
print(Monthly_VaR()) #uses Daily_Returns within the function

