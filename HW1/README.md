### myStrategy.py:
#### Returns the action of "buy" or "sell". The parameters of this function are optimized by "bestParamByExhaustiveSearch.py".

### bestParamByExhaustiveSearch.py:
#### This script obtains the best parameters by exhaustive search. You can then insert the best parameters into myStrategy.py for evaluation.
```shell
python bestParamByExhaustiveSearch.py 0050.csv
```
### rrEstimate.py:
#### This script calls myStrategy.py to obtain RR (return rate) for a given price vectors.
```shell
python rrEstimate.py 0050.csv
```
### *.csv (0050.TW.csv):
#### Price of 0050 from 2008/01/02 - 2022/10/17
