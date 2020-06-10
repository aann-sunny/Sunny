import pymssql
from model.stockmodel import StockModel

ip ='localhost' 
id ='sa'
pw ='mssql1234'
db ='FINANCE'


def SearchOne(stock_code):

    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()
    query = '''
                SELECT STOCK_CODE
                     , STOCK_NAME
                     , STOCK_CATE
                     , STOCK_SECTOR
                     , STOCK_ADDRESS
                  FROM STOCK
                 WHERE STOCK_CODE = %s
            '''

    cursor.execute(query, stock_code)

    stock_code = None 

    row = cursor.fetchone()
    while row:
        stock_one = StockModel(row[0], row[1], row[2])
        row. cursor.fetchone()

    return stock_one


def CheckExistsStock(stock_code):
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()

    query = 'SELECT * FROM STOCK WHERE STOCK_CODE = %s'
    cursor.execute(query, stock_code)
    isExists = False
    row = cursor.fetchone()

    while row:
        isExists = True
        row = cursor.fetchone()
    conn.close()

    return isExists


def SaveStock(stock):
    if stock == None:
        print('조회된 종목이 없습니다. 먼저 종목을 검색해 주세요.')
    elif CheckExistsStock(stock.stock_code) == True:
        print('({0})이미 등록된 종목입니다.'.format(stock.stock_code))
    else:

        conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
        cursor = conn.cursor()
        
        query = 'INSERT INTO STOCK (STOCK_CODE, STOCK_NAME, STOCK_CATE) VALUES (%s, %s, %s)'
        cursor.execute(query, (stock.stock_code, stock.stock_name, stock.stock_cate))
        conn.commit()
        conn.close()
        print('{0}({1}) 종목이 DB에 정상 저장되었습니다.'.format(stock.stock_name, stock.stock_code))


ip ='localhost' 
id ='sa'
pw ='mssql1234'
db ='FINANCE'



def SearchList():
    
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()

    query = 'SELECT STOCK_CODE, STOCK_NAME, STOCK_CATE FROM STOCK'
    cursor.execute(query)

    stock_list = []
    row = cursor.fetchone()
    while row:
        stock = StockModel(row[0], row[1], row[2])
        stock_list.append(stock)
        row = cursor.fetchone()

    for stock in stock_list:
        stock.PrintLine()
    
    return stock_list



def EditStock():

    code = input('수정할 대상의 종목코드를 입력해주세요: ').upper()
    
    if CheckExistsStock(code) == False:
        print('({0}) 잘못된 코드입니다.'.format(code))
    else:
        stock = SearchOne(code)
        
        print('수정할 대상 데이터')
        stock.PrintLine()
        print('-----------------')
        sector = input('Sector 입력: ')
        address = input('Address 입력: ')

        yn = input('정말 수정하시겠습니까? (y/n)')

        if yn.upper() == 'N':
            print('수정 작업 취소되었습니다. {0}'.format(code))
        
        else:   
            conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
            cursor = conn.cursor()
            
            query = '''
                        UPDATE STOCK
                           SET STOCK_SECTOR = %s
                             , STOCK_ADDRESS = %s
                         WHERE STOCK_CODE = %s 
                    '''
            
            cursor.execute(query, (sector, address, code))
            conn.commit()
            conn.close()

            print('정상적으로 저장되었습니다. {0}'.format(code))
