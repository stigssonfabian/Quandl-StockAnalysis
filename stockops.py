import os
import stocks





def stock_symbols():
    if not os.path.exists(stocks.stock_folder):
        os.mkdir(stocks.stock_folder)

    symbols = []

    for fn in os.listdir(stocks.stock_folder):
        if not fn.startswith('.'):
            symbols.append(fn.replace('.txt', ''))
    return symbols



def read_stock_data_from_dataset():
   files = os.listdir('.')

   stock_file_name = None

   for file in files:
       if file.endswith('.csv') and 'SF0' in file:
          stock_file_name = file

   if stock_file_name == None:
        return False

   stock_file = open(stock_file_name, 'r')

   lines = stock_file.read().split('\n')
   previous_symbol = lines[0].split(',')[0].split('_')[0]
   previous_item_name = lines[0].split(',')[0].split('_')[1]
   stocks = {} # contains all stocks
   company_data = {} # temporarily contains all items and dates to values
   values = {} # temporarily contains all the values and the period in which the value was recorded
   values[lines[0].split(',')[1]] = lines[0].split(',')[2]
   for i in range(1, len(lines) - 1):
       data = lines[i].split(',')
       symbol = data[0].split('_')[0]
       item_name = data[0].split('_')[1]
       date = data[1]
       val = data[2]

       if not symbol == previous_symbol:
           stocks[previous_symbol] = company_data
           company_data = {}
           previous_symbol = symbol
       if not item_name == previous_item_name:
           company_data[previous_item_name] = values
           previous_item_name = item_name
           values = {}

       values[date] = val
   return stocks


def write_stocks(stock_data={}):
    for stock_symbol, stock_data in stock_data.items():
        file = open(stocks.stock_folder + os.sep + stock_symbol + '.txt', 'w')
        output = ''
        for item_name, item_data in stock_data.items():
            output += item_name + stocks.val_sep
            soreted_item_data = sorted(item_data.items())
            for date_val in soreted_item_data:
                output += date_val[0] + stocks.pair_sep + date_val[1] + stocks.val_sep
            output = output.strip() + "\n"
        file.write(output.strip())
        file.close()

def create_stock_files():
    if not os.path.exists(stocks.stock_folder):
        os.mkdir(stocks.stock_folder)

    files = os.listdir('.')
    for f in files:
        if f.endswith('.csv') and f.startswith('SF0'):
            os.remove(f)

    write_stocks(read_stock_data_from_dataset())


def stocks_with_price_data():
    objs = read_all_stock_objects()

    stocks_with_prices = []

    for i in range(len(objs)):
        if objs[i].has_price():
            stocks_with_prices.append(objs[i])

    return stocks_with_prices



def read_all_stock_objects():
     stock_objects = []
     for name in os.listdir(stocks.stock_folder):
         if not name.startswith("."):
             symbol = name.replace('.txt', '')
             s = stocks.Stock(symbol)
             stock_objects.append(s)
     return stock_objects


