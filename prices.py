import urllib
import dateutil.parser
import datetime
import stockops
import os
import stocks


file_prices = 'prices.csv'

folder_prices = 'StockPrices'



def append_prices_in_stock_files():
    csv = open(file_prices, 'r')

    lines = csv.read().split('\n')
    headers = lines[0:1][0].split(',')[2:]
    prev_symbol = lines[1].split(',')[0]

    stock = None

    if stocks.exists(prev_symbol):
        stock = stockops.read_stock(prev_symbol)
    dates = stock.longest_dates()
    date_index = 0

    prev_data = []

    price_data = {}
    lines = lines[1:]

    print('Starting to append')

    for i in range(len(lines)):
        data = lines[i].split(',')

        if not prev_symbol == data[0] or i == len(lines) - 1:
            if not stock == None:
                print(prev_symbol)
                file = open(stockops.file_path(prev_symbol), 'a')
                file.write("\n" + price_data_to_text(price_data) + "\n" + encode_latest_price_data(prev_data[1:], headers))
                file.close()

            if stocks.exists(data[0]):
                stock = stockops.read_stock(data[0])
                dates = stock.longest_dates()
            else:
                stock = None
                dates = []

            prev_symbol = data[0]
            date_index = 0
            price_data = {}

        prev_data = data
        if not len(dates) == date_index:
            if d1_minus_d2(data[1], dates[date_index]) >= 0:
                for i in range(len(headers)):
                    if not headers[i] in price_data:
                        price_data[headers[i]] = []
                    price_data[headers[i]].append((dates[date_index], data[i + 2]))
                date_index += 1

    csv.close()

def price_data_to_text(price_data = {}):
    text = ''
    for k, v in price_data.items():
        text += k + stocks.val_sep
        v = sorted(v, key= lambda x: x[0])

        for val in v:
            text += val[0] + stocks.pair_sep + val[1] + stocks.val_sep
        text = text.strip()
        text += '\n'
    return text.strip()





def extract_price_data(dates = [], price_string = ''):
    lines = price_string.split('\n')
    headers = lines[0:1][0].split(stocks.val_sep)[1:]

    date_index = 0

    price_data = {}

    for line in lines[1:]:
        data = line.split(stocks.val_sep)

        if d1_minus_d2(data[0], dates[date_index]) >= 0:
            for i in range(len(headers)):
                if not headers[i] in price_data:
                    price_data[headers[i]] = []
                price_data[headers[i]].append((dates[date_index], float(data[i + 1])))
            date_index += 1
            if date_index == len(dates):
                return price_data

    raise Exception('price data could not be extracted' + "\n" + data + "\n" + dates[date_index] + "\n" + dates)


def encode_latest_price_data(data = [], headers = []):
    date = data[0]
    output = ''
    for i in range(len(headers)):
        output += "latest_" + headers[i] + stocks.val_sep + date + stocks.pair_sep + data[i + 1] + "\n"
    return output.strip()



def d1_minus_d2(d1, d2):
    d1 = dateutil.parser.parse(d1)
    d2 = dateutil.parser.parse(d2)
    return (d1 - d2).days




