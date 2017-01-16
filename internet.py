import urllib.request as urllib
import os
import zipfile as zip

sf0_stock_base_url = "https://www.quandl.com/api/v3/databases/SF0/data?auth_token=" #erronous



def download_stock_dataset(key):
    opener = urllib.build_opener(urllib.HTTPCookieProcessor())
    response = opener.open(sf0_stock_base_url + key)
    file = open('temp.zip', 'wb')
    file.write(response.read())
    file.close()
    zip_ref = zip.ZipFile('temp.zip')
    zip_ref.extractall(".")
    os.remove('temp.zip')
    zip_ref.close()
