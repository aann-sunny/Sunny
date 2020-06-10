class StockDetail:

    def __init__(self,_id, _stock_code, _stock_date, _stock_open, _stock_high, _stock_low, _stock_close, _stock_adj_close, _stock_volume):

        self.id = _id
        self.stock_code = _stock_code
        self.stock_date = _stock_date
        self.stock_open = _stock_open
        self.stock_high = _stock_high
        self.stock_low = _stock_low 
        self.stock_close = _stock_close
        self.stock_adj_close = _stock_adj_close 
        self.stock_volume = _stock_volume

    
    def GetTr(self):
        
        td_list = ''

        td_list += '<td>{0}</td>'.format(self.id)
        td_list += '<td>{0}</td>'.format(self.stock_code) 
        td_list += '<td>{0}</td>'.format(self.stock_date) 
        td_list += '<td>{0}</td>'.format(self.stock_open) 
        td_list += '<td>{0}</td>'.format(self.stock_high) 
        td_list += '<td>{0}</td>'.format(self.stock_low) 
        td_list += '<td>{0}</td>'.format(self.stock_close)
        td_list += '<td>{0}</td>'.format(self.stock_adj_close)
        td_list += '<td>{0}</td>'.format(self.stock_volume)

        tr = '<tr>{0}</tr>'.format(td_list)

        return tr  