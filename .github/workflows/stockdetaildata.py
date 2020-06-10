import os
import time
import pymssql
import datetime
from shutil import copyfile
from model.stockdetailmodel import StockDetail
from dataaccess.stockdata import CheckExistsStock

ip = 'localhost'
id = 'sa'
pw = 'mssql1234'
db = 'FINANCE'


def DeleteByStockCode(stock_code):
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()

    query = 'DELETE STOCK_DETAIL WHERE STOCK_CODE = %s'
    cursor.execute(query, stock_code)
    conn.commit()
    conn.close()

    print('데이터 일괄삭제: {0}'.format(stock_code))


def GetDetailList(code, dst):


    detail_list = []
    f = open(dst, encoding='utf-8')

    for line in f.readlines()[1:]:
        data_list = line.split(',')

        if data_list[1] == 'null':
            continue 

        _stock_date = datetime.datetime.strptime(data_list[0],'%Y-%m-%d')
        _stock_open = data_list[1]
        _stock_high = data_list[2]
        _stock_low = data_list[3]
        _stock_close = data_list[4]
        _stock_adj_close = data_list[5]
        _stock_volume = data_list[6].strip()

        detail = StockDetail(-1, code, _stock_date, _stock_open, _stock_high, _stock_low, _stock_close, _stock_adj_close, _stock_volume)
        detail_list.append(detail)

    return detail_list

def DownloadAndDBSave(driver):

    code = input('상세정보를 데이터베이스에 등록할 종목코드를 입력하세요').upper()

    if CheckExistsStock(code) == False:
        print('아직 등록되지 않은 종목코드입니다. \n 먼저 종목코드를 등록해주시기 바랍니다.')
    else:
        url = 'https://finance.yahoo.com/quote/{0}/history?p={0}'.format(code)
        driver.get(url)
        time.sleep(2)

        period = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span')
        period.click()
        time.sleep(1)
        maxbtn = driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button')
        maxbtn.click()
        time.sleep(1)
        applyy = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
        applyy.click()
        time.sleep(1)
        download = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
        download.click()
        time.sleep(1)

        # 'C:\finance\detail'
        # 'C:\Users\686\Downloads'

        src = r'C:\Users\686\Downloads\{0}.csv'.format(code)
        time.sleep(1)
        dst = r'C:\finance\detail\{0}.csv'.format(code)

        while os.path.isfile(src) == False:
            time.sleep(0.2)

        copyfile(src, dst)
        os.remove(src)

        detail_list = GetDetailList(code, dst)
        # 데이터 있으나마나 삭제
        DeleteByStockCode(code)

        conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
        cursor = conn.cursor()

        query = 'INSERT INTO STOCK_DETAIL (STOCK_CODE, STOCK_DATE, STOCK_OPEN, STOCK_HIGH, STOCK_LOW, STOCK_CLOSE, STOCK_ADJ_CLOSE, STOCK_VOLUME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        for d in detail_list:
            cursor.execute(query, (d.stock_code, d.stock_date, d.stock_open, d.stock_high, d.stock_low, d.stock_close, d.stock_adj_close, d.stock_volume))
            print('Added: {0} {1}'.format(d.stock_date, d.stock_code))
        conn.commit()
        conn.close()


def SearchDetailByStockCode(stock_code):
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()
    query = '''
                SELECT id
                     , STOCK_CODE
                     , STOCK_DATE
                     , STOCK_OPEN
                     , STOCK_HIGH
                     , STOCK_LOW
                     , STOCK_CLOSE
                     , STOCK_ADJ_CLOSE
                     , STOCK_VOLUME
                 FROM STOCK_DETAIL
                WHERE STOCK_CODE = %s
            '''
    cursor.execute(query, stock_code)

    detail_list = []

    row = cursor.fetchone()
    while row:
        detail = StockDetail(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        detail_list.append(detail)
        row = cursor.fetchone()
    conn.close()
    return detail_list


def CreateReportHtml():

    code = input('리포트로 저장할 종목코드를 입력하세요: ')
    detail_list = SearchDetailByStockCode(code)

    tr_list = ''
    for detail in detail_list:
        tr_list += detail.GetTr()


    style = '''
    <style>
    table{
        width: 30%
        border: 1px solid #444444;
    }
    th
    {
        background-color:wheat;
        border: 1px solid #444444;
    }
    td{
        border: 1px solid #444444;
        text-align: left;
        padding: 6px
    }
    </style>
    '''

    table = '<table>{0}</table>'.format(tr_list)
    body = '<body>{0}</body>'.format(table)
    head = '<head>{0}</head>'.format(style)
    html = '<html>{0}{1}</html>'.format(head, body)
    
    path = r'C:\python\report_{0}.html'.format(code)
    f = open(path, 'w', encoding='utf-8')
    f.write(html)
    f.close()

    os.system(path)