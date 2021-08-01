import math
import finsymbols
import yfinance as yf

companies = []
for company in finsymbols.get_sp500_symbols():
    companies.append(company['symbol'].strip('\n'))

tickers = []
i = 1
while i < 4:
    ticker = input(f"Enter ticker #{i}: ").strip('\n').upper()
    if ticker in companies:
        tickers.append(ticker)
        i += 1
    else:
        print("Invalid ticker.")

data = yf.download(tickers=tickers, period = "5y", interval="3mo")

returns = [[], [], []]
for i in range(len(tickers)):
    for price in data['Close'][tickers[i]]:
        if not math.isnan((price)):
            returns[i].append(price)
    returns[i].pop()

for company in returns:
    for i in range(len(company) - 1):
        company.append((company[1] - company[0])/company[0])
        company.pop(0)
    company.pop(0)

# Summary statistics
print("*** INDIVIDUAL ASSET CHARACTERISTICS ***\n")
for i in range(len(returns)):
    print(f"E[r] {tickers[i]}: {math.pow(1+sum(returns[i])/len(returns[i]),4)-1}")
