"""
Quantitative Modeling Framework for Python

Based on popular, but defunct quantmod R framework

May include some overlap with statsmodels
"""
import ysq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def backtest(prices, signalGenerator, capital = 10000.0, leverage = 1.0, shorting = True, reporting = True):
    signals = signalGenerator(prices)
    r = returns(prices, signals, capital, leverage)
    s = sharpe(r[1], 0.04)

    if reporting:
        report(signals, r, s)
        p(prices, signals, r)

    else:
        return signals, r, s

def returns(prices, signals, capital, leverage, shorting = True):
    result = np.zeros(len(signals))
    result[0] = capital*leverage

    for i in range(len(signals)-1):
        if signals[i] == -1 and shorting:
            # short signal
            result[i+1] = result[i]+(np.floor(result[i]/prices[i]))*(prices[i]-prices[i+1])

        elif signals[i] == 1:
            # long signal
            result[i+1] = result[i]+(np.floor(result[i]/prices[i]))*(prices[i+1]-prices[i])

        else:
            result[i+1] = result[i]

    dailyRet = (result[1:]-result[0:-1])/result[0:-1]

    return result, dailyRet

def sharpe(dailyRet, riskfree):
    excessRet = dailyRet - (riskfree/252)
    return np.sqrt(252)*np.mean(excessRet)/np.std(excessRet)

def oneStock(signalGenerator, stock):
    """
    Get the signal, portfolioValue, stockValue of one stock.

    Returns a pandas dataframe.
    """
    
    close = ysq.dfTwoYearClose(stock)
    result = backtest(close, signalGenerator, reporting = False)
    df = pd.DataFrame(result[0]) # the signal
    df['portfolioValue'] = result[1][0]
    df['stockValue'] = close
    return df

def saveStockCsv(signalGenerator, stock):
    oneStock(signalGenerator, stock).to_csv("results.csv")

def picker(signalGenerator, startingIndex, endingIndex, pathToData):
    with open(pathToData, 'r') as f:
        stocks = f.readlines()

    for i in range(len(stocks)):
        stocks[i] = stocks[i].rstrip()

    results = {}

    for row in stocks[startingIndex:endingIndex]:
        close = ysq.dfTwoYearClose(row)
        results[row] = backtest(close, signalGenerator, reporting = False)

    maxSymbol = None
    maxSharpe = 0.0

    for symbol in results:
        if results[symbol][2] > maxSharpe:
            maxSymbol = symbol
            maxSharpe = results[symbol][2]

    print maxSymbol
    report(results[maxSymbol][0], results[maxSymbol][1], results[maxSymbol][2])
    p(ysq.dfTwoYearClose(maxSymbol), results[maxSymbol][0], results[maxSymbol][1][0])

def nasPicker(signalGenerator):
    picker(signalGenerator, 0, 20,'./nas100.txt')

def spPicker(signalGenerator):
    picker(signalGenerator, 0, 50, './sp500.txt')

def report(signals, returns, sharpe):

    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Starting Capital:', returns[0][0]
    print 'Ending Capital:', returns[0][-1]
    print 'Total Number of Trades:', ((signals == -1).sum())+((signals == 1).sum())
    print 'Total Gain (Percentage):', ((returns[0][-1]/returns[0][0])-1)*100
    print 'Average Daily Gain (Percentage):', (((returns[0][-1]/returns[0][0])-1)/len(returns))*100
    print 'Average Annual Gain (Percentage):', ((((returns[0][-1]/returns[0][0])-1)/len(returns))*252)*100
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Sharpe Ratio:', sharpe
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Number of Drawdowns:', 0
    print 'Average Drawdown:', 0
    print 'Max Drawdown:', 0
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Number of Short Trades:', (signals == -1).sum()
    print 'Number of Short Winners:', 0 
    print 'Average Short Trade Profit (Total):', 0 
    print 'Average Short Trade Profit (Winners):', 0
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Number of Long Trades:', (signals == 1).sum()
    print 'Number of Long Winners:', 0
    print 'Average Long Trade Profit (Total):', 0
    print 'Average Long Trade Profit (Winners):', 0
    print '+++++++++++++++++++++++++++++++++++++++++++++++'


def p(prices, signals, returns):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(returns)
    plt.subplot(212)
    plt.plot(prices)
    for i in range(len(signals)):
        if signals[i] == -1:
            #Draw Redline
            plt.axvline(i, color = 'r')

        elif signals[i] == 1:
            #Draw Greenline
            plt.axvline(i, color = 'g')

    plt.show()

def setBuilder(series, trainSize):
    s = np.asarray(series)
    numRows = np.floor(len(series)/(trainSize+1))
    newS = s[:numRows*(trainSize+1)]
    newS = newS.reshape(-1, trainSize+1)

    training = newS[:,0:trainSize+1]
    test = newS[:,trainSize:]

    return training, test
    
