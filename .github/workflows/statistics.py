import pymssql
from dataaccess.stockdata import SearchOne

ip = 'localhost'
id = 'sa'
pw = 'mssql1234'
db = 'FINANCE'

def SearchByStockDay():
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()
    query = '''
              SELECT D.STOCK_CODE
                   , S.STOCK_NAME
                   , S.STOCK_CATE
                   , COUNT(*) AS DAY_COUNT
                FROM STOCK_DETAIL D
                JOIN STOCK S 
                  ON D.STOCK_CODE = S.STOCK_CODE
            GROUP BY D.STOCK_CODE, S.STOCK_NAME, S.STOCK_CATE
            ORDER BY DAY_COUNT DESC
            '''

    cursor.execute(query)
    row = cursor.fetchone()
    while row: 
        print('{0:>6} {1:<30} {2} {3}'.format(row[0], row[1], row[2], row[3]))
        print('---------------')
        row = cursor.fetchone()

    
def SearchHigh():
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()
    query = '''
              SELECT STOCK_CODE
                   , MAX(STOCK_HIGH) AS MAX
                   , MIN(STOCK_HIGH) AS MIN
                FROM STOCK_DETAIL 
            GROUP BY STOCK_CODE
            ORDER BY MAX DESC
            '''

    cursor.execute(query)
    row = cursor.fetchone()
    while row: 
        print('{0:<6} {1:>15.2f} {2} '.format(row[0], float(row[1]), float(row[2])))
        print('---------------')
        row = cursor.fetchone()
        

def MaxVolumeDate():
    conn = pymssql.connect(server=ip, user=id, password=pw, database=db)
    cursor = conn.cursor()
    query = '''
              SELECT S.STOCK_CODE
                   , MAX(S.STOCK_VOLUME) AS MAX 
                   , (SELECT TOP 1 A.STOCK_DATE 
                FROM STOCK_DETAIL A 
                    WHERE A.STOCK_VOLUME = MAX(S.STOCK_VOLUME)) AS MAX_DAY
                FROM STOCK_DETAIL S
            GROUP BY STOCK_CODE
            '''

    cursor.execute(query)
    row = cursor.fetchone()
    while row: 
        print('{0} {1} {2} '.format(row[0], row[1], row[2]))
        print('---------------')
        row = cursor.fetchone()