import math
import os

stock_folder = "Companies"

val_sep = '\t'
pair_sep = ','




def rank_stocks(average_stock_data, stock_objects):

    stock_ranking = []

    lim = 1.7

    for stock in stock_objects:

        points = 0

        for avg in average_stock_data:
            if len(avg) == 2:
                grade = growth(stock, avg[0]) / avg[1]
                if grade > lim:
                    grade = lim
                if grade < 0:
                    grade = 0
                points += grade
            elif len(avg) == 3 and not stock.get_latest_value(avg[1]) == 0:
                grade = div(stock, avg[0], avg[1]) / avg[2]
                if grade > lim:
                    grade = lim
                if grade < 0:
                    grade = 0
                points += grade

        stock_ranking.append((points, stock))

    return stock_ranking


def div(stock, indicator_num, indicator_denom):
    return stock.get_latest_value(indicator_num) / stock.get_latest_value(indicator_denom)

def growth(stock, indicator):
    return stock.flat_growth(indicator)

def average(stock_objects):
    growth_avgs = ['REVENUEUSD', 'NETINCCMNUSD', 'EQUITYUSD']
    avgs = [('RND', 'market_cap'),
            ('EPSUSD', 'latest_adj_close'),
            ('DPS', 'latest_adj_close'),
            ('NCF', 'market_cap'),
            ('ASSETS', 'market_cap'),
            ('CASHNEQUSD', 'market_cap'),
            ('market_cap', 'DEBTUSD'),
            ('EQUITYUSD', 'market_cap'),]

    growth_avgs = ['REVENUEUSD']
    avgs = [('DPS', 'latest_adj_close'),
            ('EQUITYUSD', 'market_cap'),
            ('EPSUSD', 'latest_adj_close'),
            ('market_cap', 'DEBTUSD'),
            ('EQUITYUSD', 'DEBTUSD')

            ]

    avg_data = []

    for ga in growth_avgs:
        avg_data.append((ga, growth_avg(ga, stock_objects)))

    for avg in avgs:
        avg_data.append((avg[0], avg[1], div_avg(avg[0], avg[1], stock_objects)))

    return avg_data


def growth_avg(indicator, stock_objects):
    total = 0
    counter = 0

    for stock in stock_objects:
        g = stock.flat_growth(indicator)
        if g > 0:
            total += g
            counter += 1

    return g / counter


def div_avg(indicator_numerator, indicator_denominator, stock_objects):
    total = 0
    counter = 0
    for stock in stock_objects:
        if not stock.get_latest_value(indicator_denominator) == 0 and not stock.get_latest_value(indicator_numerator) < 0:
            total += stock.get_latest_value(indicator_numerator) / stock.get_latest_value(indicator_denominator)
            counter += 1
    return total / counter


def exists(symbol):
    if os.path.exists(stock_folder + os.sep + symbol + '.txt'):
        return True
    else:
        return False

class Stock:

    item_data = None
    symbol = None

    def __init__(self, symbol = None):
        symbol = symbol.upper()
        self.item_data = {}

        financial_file = open(stock_folder + os.sep + symbol + ".txt", 'r')
        stock_string = financial_file.read()

        for line in stock_string.split('\n'):
            vals = line.split(val_sep)
            date_values = []
            for i in range(1, len(vals)):
                date_val = vals[i].split(pair_sep)
                date_values.append((date_val[0], float(date_val[1])))
            self.item_data[vals[0]] = date_values
        self.symbol = symbol

        if self.has_price():
            self.item_data['market_cap'] = [(self.item_data['adj_close'][0][0], self.current_market_cap())]

    def print_detailed(self):

        output = '******** ' + self.symbol + '********'
        sep = '\t'
        dates = self.longest_dates()
        output += '\n'
        for d in dates:
            output += d + sep
        output = output.strip()

        for k, v in self.item_data.items():
            output += '\n' + k + sep

            for value in v:
                output += str(value[1]) + sep

            output = output.strip()

        print(output)




    def print_key_data(self):
        output = ''
        print('*********** ' + self.symbol + ' *********')
        print('Market Cap = ' + str(self.current_market_cap() / 1000000000) + " Bil")
        print('PE - Ratio = ' + str(round(self.pe_ratio(), 3)))
        print('Growth Revenue = ' + str(round(self.flat_growth('REVENUE'), 3)) + "%")
        print('Growth Equity = ' + str(round(self.flat_growth('EQUITYUSD'), 4)))
        print('Debt to Equity = ' + str(round(self.get_latest_value('DE'), 4)))
        print('Equity / Market Cap = ' + str(round(self.book_to_market_cap(), 4)))
        print('Debt / Market Cap = ' + str(round(self.debt_to_market_cap(), 3)))
        print('Dividend Yield = ' + str(round(self.dividend_yield() * 100, 4)) + '%')
        print('Free Cash Flow / Market Cap = ' + str(self.get_latest_value('FCF') / self.current_market_cap()))
        print('Cash and Equivalents / Market Cap = ' + str(round(self.get_latest_value('CASHNEQ') / self.current_market_cap(), 4)))

    def has_price(self):
        return 'open' in self.item_data

    def period_length(self, indicator):
        return len(self.item_data[indicator])

    def get_item_vals(self, indicator):
        return self.item_data[indicator]

    def get_value_at(self, indicator, index):
        return self.get_item(indicator)[index][1]

    def get_date_for(self, indicator, index):
        return self.get_item(indicator)[index][0]

    def get_dates_for(self, indicator):
        dates = []
        for date_val in self.get_item_vals(indicator):
            dates.append(date_val[0])
        return dates


    def flat_growth(self, indicator):
        items = self.item_data[indicator]

        tot = 0

        counter = 0

        for i in range(len(items) - 1):
            counter += 1
            if items[i + 1][1] == 0 or items[i][1] == 0:
                continue
            tot += (items[i + 1][1] - items[i][1]) / items[i + 1][1]

        if counter == 0:
            return 0

        if tot / counter < 0:
            return 0

        return tot / counter

    def growth_and_period(self, indicator = ''):
        items = self.item_data[indicator]
        period_length = -1
        for i in range(len(items) - 1, 0, -1):
            if items[i][1] <= 0:
                break
            elif items[i][1] >= items[i - 1][1]:
                period_length += 1
            else:
               break

        if period_length == 0:
            return (0, 0)
        if period_length == -1:
            return (0,0)

        return (period_length, math.pow(items[len(items) - 1][1] / items[len(items) - 1 - period_length][1], 1 / period_length))

    def get_latest_value(self, indicator):
        return self.item_data[indicator][len(self.item_data[indicator]) - 1][1]


    def market_cap_latest_reported_data(self):
       return self.get_latest_value('SHARESWADIL') * self.get_latest_value('adj_close')

    def current_market_cap(self):
        k = ''

        if 'SHARESWADIL' in self.item_data:
            k = 'SHARESWADIL'
        else:
            k = 'SHARESWA'

        return self.get_latest_value(k) * self.get_latest_value('latest_adj_close')

    def pe_ratio(self):
        return self.get_latest_value('latest_adj_close') / self.get_latest_value('EPSUSD')

    def book_to_market_cap(self):
        return self.get_latest_value('EQUITYUSD') / self.current_market_cap()

    def dividend_yield(self):
        return self.get_latest_value('DPS') / self.get_latest_value('latest_adj_close')

    def debt_to_market_cap(self):
        return self.get_latest_value('DEBTUSD') / self.current_market_cap()

    def roe(self):
        return self.get_latest_value('NETINCCMNUSD') / self.get_latest_value('EQUITYUSD')

    def indicators(self):
        return self.item_data.keys()

    def longest_dates(self):
        longetst_dates = []
        for indicator in self.item_data.keys():
            temp = self.get_dates_for(indicator)
            if len(temp) > len(longetst_dates):
                longetst_dates = temp
        return temp









