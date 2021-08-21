import math
import statistics
import numpy
import finsymbols
import yfinance as yf

class Portfolio:

    def __init__(self, stocks):
        self.stocks = stocks
        self.weights = [1/3, 1/3, 1/3]
        self.indv_returns = [[], [], []]
        self.indv_stdevs = []
        self.set_indv_attributes()
        self.p_return = 0.0
        self.p_stdev = 0.0
        self.set_portfolio_return()
        self.set_portfolio_stdev()


    def set_indv_attributes(self):
        # Puts relevant prices into 2D array 'returns'
        for i in range(len(self.stocks)):
            for price in data['Close'][self.stocks[i]]:
                if not math.isnan((price)):
                    self.indv_returns[i].append(price)
            self.indv_returns[i].pop()

        # Iterates through returns, changing the actual prices to the percent change between periods
        for company in self.indv_returns:
            for i in range(len(company) - 1):
                company.append((company[1] - company[0]) / company[0])
                company.pop(0)
            company.pop(0)

        # Calculate standard deviation in returns for each individual stock
        for i in range(len(self.stocks)):
            self.indv_stdevs.append(statistics.stdev(self.indv_returns[i]))

    # Calculate expected annual return of three-stock portfolio
    def set_portfolio_return(self):
        annualized = 0.0
        for i in range(3):
            annualized += (math.pow(1 + sum(self.indv_returns[i]) / len(self.indv_returns[i]), 4) - 1) * self.weights[i]
        self.p_return = annualized

    # Calculates standard deviation of three-stock portfolio
    def set_portfolio_stdev(self):
        result = 0.0
        for i in range(3):
            result += math.pow(self.weights[i], 2) * math.pow(self.indv_stdevs[i], 2)
        result += 2 * numpy.corrcoef(self.indv_returns[0], self.indv_returns[1])[0][1] * self.weights[0] * self.weights[1] * self.indv_stdevs[0] * self.indv_stdevs[1]
        result += 2 * numpy.corrcoef(self.indv_returns[0], self.indv_returns[2])[0][1] * self.weights[0] * self.weights[2] * self.indv_stdevs[0] * self.indv_stdevs[2]
        result += 2 * numpy.corrcoef(self.indv_returns[1], self.indv_returns[2])[0][1] * self.weights[1] * self.weights[2] * self.indv_stdevs[1] * self.indv_stdevs[2]
        self.p_stdev = math.pow(1 + result, 4) - 1

if __name__ == '__main__':
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

    # Create Portfolio object out of 3 stocks
    portfolio = Portfolio(tickers)

    # Print portfolio characteristics
    print(f"\n\nE[r]p: {portfolio.p_return}")
    print(f"σ(p): {portfolio.p_stdev}")
