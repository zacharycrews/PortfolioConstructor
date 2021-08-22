import math
import statistics
import numpy
import finsymbols
import yfinance as yf
from scipy.optimize import minimize, LinearConstraint, Bounds

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
        self.set_portfolio_stdev(self.weights)

    # Calculates annual returns and corresponding standard deviations for each stock
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

        # Annualizes returns
        for company in self.indv_returns:
            original_len = len(company)
            for i in range(int(len(company) / 4)):
                company.append((1+company[0])*(1+company[1])*(1+company[2])*(1+company[3])- 1)
                for j in range(4):
                    company.pop(0)
            while len(company) != int(original_len / 4):
                company.pop(0)

        # Calculates standard deviation of each stock using annual returns
        for i in range(len(self.stocks)):
            self.indv_stdevs.append(statistics.stdev(self.indv_returns[i]))

    # Calculate expected annual return of three-stock portfolio
    def set_portfolio_return(self):
        total_return = 0.0
        for i in range(3):
            total_return += sum(self.indv_returns[i]) / len(self.indv_returns[i]) * self.weights[i]
        self.p_return = total_return

    # Calculates standard deviation of three-stock portfolio
    def set_portfolio_stdev(self, weights, *args):
        result = 0.0
        for i in range(3):
            result += math.pow(weights[i], 2) * math.pow(self.indv_stdevs[i], 2)
        result += 2 * numpy.corrcoef(self.indv_returns[0], self.indv_returns[1])[0][1] * weights[0] * weights[1] * self.indv_stdevs[0] * self.indv_stdevs[1]
        result += 2 * numpy.corrcoef(self.indv_returns[0], self.indv_returns[2])[0][1] * weights[0] * weights[2] * self.indv_stdevs[0] * self.indv_stdevs[2]
        result += 2 * numpy.corrcoef(self.indv_returns[1], self.indv_returns[2])[0][1] * weights[1] * weights[2] * self.indv_stdevs[1] * self.indv_stdevs[2]
        self.p_stdev = math.sqrt(result)
        return self.p_stdev

    # Minimizes portfolio risk by finding optimal stock weights
    def optimize_weights(self):
        bounds = Bounds([0,0,0], [1,1,1])
        constraint = LinearConstraint([1,1,1], [1], [1])
        res = minimize(self.set_portfolio_stdev, x0 = self.weights, method='trust-constr', constraints = constraint, bounds = bounds)
        self.weights = res.x
        self.set_portfolio_return()

    # Prints portfolio characteristics
    def print_stats(self):
        print(f"Weights: \t{self.stocks[0]}- {'{:.2%}'.format(self.weights[0])} \n\t\t\t"
                + f"{self.stocks[1]}- {'{:.2%}'.format(self.weights[1])} \n\t\t\t"
                + f"{self.stocks[2]}- {'{:.2%}'.format(self.weights[2])}")
        print(f"\nE[r]p: \t\t{'{:.2%}'.format(self.p_return)}")
        print(f"σ(p): \t\t{'{:.2%}'.format(self.p_stdev)}")

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
    data = yf.download(tickers = tickers, period = "5y", interval = "3mo", progress = False)

    # Creates Portfolio object out of 3 stocks
    portfolio = Portfolio(tickers)

    # Prints pre- and post-optimization portfolio characteristics
    print("\n\n*** UNWEIGHTED PORTFOLIO***")
    portfolio.print_stats()
    portfolio.optimize_weights()
    print("\n\n*** OPTIMIZED PORTFOLIO***")
    portfolio.print_stats()
