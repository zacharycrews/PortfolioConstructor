import math
import statistics
import numpy
import finsymbols
import yfinance as yf

# Calculates standard deviation of three-stock portfolio
def portfolio_stdev(weights, returns, stdevs) -> float:
    result = 0.0
    for i in range(3):
        result += math.pow(weights[i],2) * math.pow(stdevs[i],2)
    result += 2 * numpy.corrcoef(returns[0],returns[1])[0][1] * weights[0] * weights[1] * stdevs[0] * stdevs[1]
    result += 2 * numpy.corrcoef(returns[0], returns[2])[0][1] * weights[0] * weights[2] * stdevs[0] * stdevs[2]
    result += 2 * numpy.corrcoef(returns[1], returns[2])[0][1] * weights[1] * weights[2] * stdevs[1] * stdevs[2]
    return math.sqrt(result)

# Gets all companies in S&P 500 index
companies = []
for company in finsymbols.get_sp500_symbols():
    companies.append(company['symbol'].strip('\n'))

# Prompts user to enter three stocks
tickers = []
i = 1
while i < 4:
    ticker = input(f"Enter ticker #{i}: ").strip('\n').upper()
    if ticker in companies:
        tickers.append(ticker)
        i += 1
    else:
        print("Invalid ticker.")

# Downloads historical price data for chosen stocks
data = yf.download(tickers=tickers, period = "5y", interval="3mo")

# Puts relevant prices into 2D array 'returns'
returns = [[], [], []]
for i in range(len(tickers)):
    for price in data['Close'][tickers[i]]:
        if not math.isnan((price)):
            returns[i].append(price)
    returns[i].pop()

# Iterates through returns, changing the actual prices to the percent change between periods
for company in returns:
    for i in range(len(company) - 1):
        company.append((company[1] - company[0])/company[0])
        company.pop(0)
    company.pop(0)

# Summary statistics
print("*** INDIVIDUAL ASSET CHARACTERISTICS ***\n")
exp_ann = []
stdevs = []
for i in range(len(returns)):
    exp_ann.append(math.pow(1+sum(returns[i])/len(returns[i]),4) - 1)
    stdevs.append(statistics.stdev(returns[i]))
    print(f"E[r] {tickers[i]}: {exp_ann[i]}")
    print(f"σ(r) {tickers[i]}: {stdevs[i]}\n")

print("*** UNWEIGHTED PORTFOLIO CHARACTERISTICS ***\n")
print(f"E[r]p: {sum(exp_ann)/len(exp_ann)}")
print(f"σ(p): {portfolio_stdev([1/3,1/3,1/3], returns, stdevs)}")
