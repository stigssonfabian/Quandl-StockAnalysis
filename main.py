import internet
import stockops
import stocks
import prices




internet.download_stock_dataset('YOUR KEY') # downloads the SF0 dataset from quandl with your api key

stockops.create_stock_files() # creates files with structured stock_data

prices.append_prices_in_stock_files() # appends stock prices to the stock files, you will need to download the price dataset from the EOD dataset
# from quandl and place the csv file in the working directory for this method to work

stock_objects = stockops.stocks_with_price_data() # reads all the stock files that have price data

ranking = stocks.rank_stocks(stocks.average(stock_objects), stock_objects) # ranks the stocks based on the average of all stocks

ranking = sorted(ranking, key= lambda x : x[0] * -1)

# prints stock data

print(ranking[0][0], ranking[0][1].symbol)
for i in range(len(ranking)):
    if ranking[i][1].flat_growth('REVENUEUSD') > 0.05 and ranking[i][1].pe_ratio() < 20:
        ranking[i][1].print_key_data()
        print('Rating = ', ranking[i][0])


