import sys
import numpy as np
import pandas as pd
import talib
from tqdm import trange

# Decision of the current day by the current price, with 3 modifiable parameters
def myStrategy(pastPriceVec, currentPrice, timeperiod, alpha, beta):
	action=0	# action=1(buy), -1(sell), 0(hold), with 0 as the default action

	PriceVec = np.append(pastPriceVec, currentPrice)

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

# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, windowSize, alpha, beta):
	capital=1000	# Initial available capital
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, windowSize, alpha, beta)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

if __name__=='__main__':
	returnRateBest=-1.00	 # Initial best return rate
	df=pd.read_csv(sys.argv[1])	# read stock file
	adjClose=df["Adj Close"].values		# get adj close as the price vector
	timeperiodMIN=5; timeperiodMAX=30;	# Range of windowSize to explore
	alphaMin=50; alphaMax=100;			# Range of alpha to explore
	betaMin=0; betaMax=50				# Range of beta to explore
	# Start exhaustive search
	for timeperiod in trange(timeperiodMIN, timeperiodMAX+1):		# For-loop for windowSize
		for alpha in range(alphaMin, alphaMax+1):	    	# For-loop for alpha
			for beta in range(betaMin, betaMax+1):		# For-loop for beta
				returnRate=computeReturnRate(adjClose, timeperiod, alpha, beta)		# Start the whole run with the given parameters
				if returnRate > returnRateBest:		# Keep the best parameters
					timeperiodBest=timeperiod
					alphaBest=alpha
					betaBest=beta
					returnRateBest=returnRate
	print("Best settings: windowSize=%d, alpha=%d, beta=%d ==> returnRate=%f" %(timeperiodBest,alphaBest,betaBest,returnRateBest))		# Print the best result
