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
    def get_collection(self, db, collection):
        client = MongoClient(constant.db_host, constant.db_port)
        db = client[db]
        return db[collection]

    def get_stock_array(self, db, collection, code=constant.stock_code):
        stock_collection = self.get_collection(db, collection)
        rows = stock_collection.find({"code": code}).sort([("date", DESCENDING)])
        date_list = list()
        percent_list = list()
        open_close_list = list()
        high_list = list()
        open_close_high = list()
        for item in rows:
            if collection == constant.db_ali_collection:
                date_list.append(item['date'])
                open_close_list.append((item['open_price'] + item['close_price']) / 2.0)
            else:
                date_list.append(item['date'])
                # percent_list.append(item['percent'])
                # high_list.append(item['high'])
                # open_close_high.append((item['open'] + item['close'] + item['high']) / 3.0)
                open_close_list.append((item['open'] + item['close']) / 2.0)

        date_array = np.array(date_list)
        percent_array = np.array(percent_list)
        stock = stock_bean.stock()
        stock.setdate(np.array(open_close_high), date_array, percent_array, constant.type_three)
        stock.add_price_data(np.array(high_list), constant.type_high)
        stock.add_price_data(np.array(open_close_high), constant.type_three)
        stock.add_price_data(np.array(open_close_list), constant.type_open)
        return stock

    def get_stock_list(self, db, collection):
        stock_collection = self.get_collection(db, collection)
        rows = stock_collection.find().sort([("date", DESCENDING)])
        data_list = list()
        for item in rows:
            data_list.append(item['code'])
        return data_list

    def insert_predict_value(self, db, collection, document):
        predict_collection = self.get_collection(db, collection)
        predict_collection.insert_one(document)


# dao = StockDao()
# result = StockDao.get_stock_list(dao, constant.db_database, constant.stock_list)
# for code in result:
#     stock_data = StockDao.get_stock_array(dao, constant.db_database, constant.db_ali_collection, float(code))
#     if (stock_data.get_size() != 0):
#         print(stock_data)
