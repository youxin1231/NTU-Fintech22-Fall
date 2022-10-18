import numpy as np
import talib

def myStrategy(pastPriceVec, currentPrice):
	# Explanation of my approach:
	# 1. Technical indicator used: MACD
	# 2. if price-ma>alpha ==> buy
	#    if price-ma<-beta ==> sell
	# 3. Modifiable parameters: alpha, beta, and window size for MA
	# 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
	
	# Set best parameters
	action=0	# action=1(buy), -1(sell), 0(hold), with 0 as the default action

	PriceVec = np.append(pastPriceVec, currentPrice)
	
	timeperiod = 30
	alpha = 65
	beta = 25

	dataLen=len(PriceVec)	# Length of the data vector
	if dataLen < timeperiod:
		action = 0
	else:
		# Compute long RSI
		rsilist_long = talib.RSI(PriceVec[-(timeperiod+1):], timeperiod)
		rsi_long = rsilist_long[-1]

		# Determine actions based on long term RSI
		if (rsi_long > alpha):
			action = 1
		elif (rsi_long < beta):
			action = -1
			
	return action
