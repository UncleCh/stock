from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo import ASCENDING
from datetime import timedelta
from datetime import datetime
import tushare as ts
import numpy as np
import time
from py.com import constant
from py.com import stock_bean


class StockDao:
    def get_stock_data(self, db, collection, code):
        stock_collection = self.get_collection(db, collection)
        data_count = stock_collection.count()
        start_date = None
        end_date = None
        if data_count != 0:
            row = stock_collection.find().sort([("date", DESCENDING)]).limit(1)
            for item in row:
                start_date = item['date']
                start_date = datetime.strptime(start_date, constant.date_format) + timedelta(days=1)
                end_date = time.strftime(constant.date_format)
                week = start_date.weekday()
                if week == 5 or week == 6 or start_date == datetime.now():
                    return stock_collection.find().sort([('date', ASCENDING)])
                else:
                    start_date = start_date.strftime(constant.date_format)
        if start_date == None and end_date == None:
            print('first get stock data')
            df = ts.get_k_data(code)
        elif start_date > end_date:
            return stock_collection.find().sort([('date', ASCENDING)])
        else :
            print('add stock data from internet start_date %s end_date %s' % start_date, end_date)
            df = ts.get_k_data(code, start_date, end_date)
        stocks = list()
        for i in df.index:
            data_row = df.ix[i]
            dict_data = dict(data_row)
            percent = (dict_data['close'] - dict_data['open']) / dict_data['open']
            percent = float('%.5f' % percent)
            dict_data['percent'] = percent
            stocks.append(dict_data)
        self.get_collection(db, collection).insert_many(stocks)
        print('return stock data')
        return stock_collection.find().sort([('date', ASCENDING)])

    def get_collection(self, db, collection):
        client = MongoClient(constant.db_host, constant.db_port)
        db = client[db]
        return db[collection]

    def get_stock_array(self, db, collection, code=constant.stock_code):
        rows = self.get_stock_data(db, collection, code)
        date_list = list()
        percent_list = list()
        open_close_list = list()
        high_list = list()
        open_close_high = list()
        for item in rows:
            if collection == constant.db_ali_collection:
                date_list.append(item['date'])
                percent_list.append(item['inc_percent'])
                high_list.append(item['max_price'])
                open_close_high.append((item['open_price'] + item['close_price'] + item['max_price']) / 3.0)
                open_close_list.append((item['open_price'] + item['close_price']) / 2.0)
            else:
                date_list.append(item['date'])
                percent_list.append(item['percent'])
                high_list.append(item['high'])
                open_close_high.append((item['open'] + item['close'] + item['high']) / 3.0)
                open_close_list.append((item['open'] + item['close']) / 2.0)

        date_array = np.array(date_list)
        percent_array = np.array(percent_list)
        stock = stock_bean.stock()
        stock.setdate(np.array(open_close_high), date_array, percent_array, constant.type_three)
        stock.add_price_data(np.array(high_list), constant.type_high)
        stock.add_price_data(np.array(open_close_high), constant.type_three)
        stock.add_price_data(np.array(open_close_high), constant.type_open)
        return stock

    def insert_predict_value(self, db, collection, document):
        predict_collection = self.get_collection(db, collection)
        predict_collection.insert_one(document)

# dao = StockDao()
# stock_data = StockDao.get_stock_array(dao,constant.db_database,constant.db_tushare_collection)
