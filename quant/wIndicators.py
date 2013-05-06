"""
Working List of Signals

All signal development is done in this file
"""

import numpy as np
import pandas as pd
import ysq

# Indicator functions.
# priceSeries is a pandas Series object.
def meanReversion(priceSeries, period = 5, mulFactor = 1, addFactor = 0):
    frame = pd.DataFrame(priceSeries)
    frame.columns = ['price']
    frame['change'] = priceSeries.diff()
    frame['sd'] = pd.rolling_std(frame['price'], period)
    frame['signal'] = np.where(frame['change'] < (mulFactor*frame['sd']+addFactor), 1, -1)
    frame['signal'][0:(period-1)] = 0

    return frame['signal']
    
    
def roundNumbers(priceSeries, period = 5, mulFactor = 1, addFactor = 0):
    frame = pd.DataFrame(priceSeries)
    frame.columns = ['price']
    frame['change'] = priceSeries.diff()
    frame['sd'] = pd.rolling_std(frame['price'], period)
    frame['signal'] = np.where(frame['change'] < (mulFactor*frame['sd']+addFactor), 1, -1)
    frame['signal'][0:(period-1)] = 0

    return frame['signal']

lastOpen = 0.0
def roundNumbers(priceSeries,stock = 'goog'):
	global lastOpen
	data = ysq.get_all('goog')
	frame = pd.DataFrame(priceSeries)
	frame.columns = ['price']
	closePrice = data['close']
	openPrice = data['open']
	high = data['high']
	closeLT = closePrice<round_stock(closePrice)
	openLT = openPrice < round_stock(openPrice)
	highGT = high > round_stock(high)
	lastCheck = (0<abs(lastOpen-round_stock(lastOpen))) and (abs(lastOpen-round_stock(lastOpen))<30)
	if(closeLT and openLT and highGT and lastCheck):
		frame['signal'] = 1
	elif (not closeLT and not openLT and not highGT and not lastCheck):
		frame['signal'] = -1
	else:
		frame['signal'] = 0
	lastOpen = data['open']
	return frame['signal']

def round_stock(x):
	if(abs(x-round(x,-2)<25)):
		return round(x,-2)
	elif (x<round(x,-2)):
		return round(x,-2)-50
	else:
		return round(x,-2)+50


def maCrossover(priceSeries, period = 3):
    return 0

# General Indicator Classes

	

