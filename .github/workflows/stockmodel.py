class StockModel:

    def __init__(self, _stock_code, _stock_name, _stock_cate, _stock_sector = '', _stock_address = ''):
        self.stock_code = _stock_code
        self.stock_name = _stock_name
        self.stock_cate = _stock_cate
        self.stock_sector = _stock_sector
        self.stock_address = _stock_address

    def PrintLine(self):
        line = '{0} {1} {2} {3} {4}'.format(self.stock_code, self.stock_name, self.stock_cate, self.stock_sector, self.stock_address)
        print(line)
        print('----------------------------')

    def ReturnTextLine(self):

        line = '{0};{1};{2};{3};{4}\n'.format(self.stock_code, self.stock_name, self.stock_cate, self.stock_sector, self.stock_address)

        return line 