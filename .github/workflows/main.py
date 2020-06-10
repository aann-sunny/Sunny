import time
import pymssql
import datetime
from selenium import webdriver
from model.stockmodel import StockModel
from dataaccess.stockdata import SaveStock, SearchList, EditStock, CheckExistsStock
from dataaccess.stockdetaildata import DownloadAndDBSave, DeleteByStockCode, CreateReportHtml
from dataaccess.statistics import SearchByStockDay, SearchHigh

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options)

LastSerachStock = None

def SearchYahoo():
    stock_code = input('검색할 종목 코드를 입력하세요: ')
    url = 'https://finance.yahoo.com/quote/{0}?p={0}&.tsrc=fin-srch'.format(stock_code)
    driver.get(url)

    time.sleep(2)
    title = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
    cate =driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span')
    
    _stock_code = title.text.split('(')[1].replace(')', '').strip()
    _stock_name = title.text.split('(')[0].strip()
    _stock_cate = cate.text.split('-')[0].strip()

    stock = StockModel(_stock_code, _stock_name, _stock_cate)
    
    return stock

#######################################################################S

command = ''

while command.upper() != 'EXIT':
    
    command = input('메뉴를 입력해주세요.')
    if command == '1':
        SearchList()
    elif command =='2':
        LastSerachStock = SearchYahoo()
        SaveStock(LastSerachStock)
    elif command == '3':
        DownloadAndDBSave(driver)
    elif command == '11':
        SearchByStockDay()
    elif command == '12':
        SearchHigh()
    elif command == '21':
        EditStock()
    elif command == '31':
        CreateReportHtml()

now = datetime.datetime.today()
print('프로그램을 종료니다. {0}'.format(now))
