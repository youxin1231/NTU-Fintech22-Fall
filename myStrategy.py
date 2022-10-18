import numpy as np
import talib

def myStrategy(pastPriceVec, currentPrice):
	# Explanation of my approach:
	# 1. Technical indicator used: MACD
	# 2. if RSI > alpha ==> buy
	#    if RSI < -beta ==> sell
	# 3. Modifiable parameters: alpha, beta, and time period of MA
	# 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
	
	# Set best parameters
	action=0	# action=1(buy), -1(sell), 0(hold), with 0 as the default action

	PriceVec = np.append(pastPriceVec, currentPrice)
	
	long_period = 22
	short_period = 7
	alpha = 62
	beta = 30
	# The performance of Golden Cross / Death Cross
	x = 1
	y = 1

	dataLen=len(PriceVec)	# Length of the data vector
	if dataLen < long_period:
		action = 0
	else:
		# Compute long RSI
		rsilist_long = talib.RSI(PriceVec[-(long_period+1):], long_period)
		rsi_long = rsilist_long[-1]

		# Compute short RSI
		rsilist_short = talib.RSI(PriceVec[-(short_period+1):], short_period)
		rsi_short = rsilist_short[-1]

		# Determine action

		# Based on long term RSI
		if (rsi_long > alpha):
			action = 1
		elif (rsi_long < beta):
			action = -1
			
		# Check if there's a Golden Cross / Death Cross
		if (rsi_short - rsi_long > x):
			action = 1
		elif (rsi_short - rsi_long < -y):
			action = -1

	return action
