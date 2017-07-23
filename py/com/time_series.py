import numpy as np
import numpy.fft as fft
from py.com import mongtest
from datetime import datetime
from py.com import constant
from datetime import timedelta
from py.com import stock_bean


def calc_periodicity(data, temporal_window=42014.0, debug=False, tryCount=1):
    length = len(data)
    suggest_value = temporal_window / length  # should equal roughly 120 seconds
    print("data length %s, shouuld equal roughly 120 seconds actual value %s" % (length, suggest_value))
    if debug:
        wave_lenght = 60 * 60 * 1  # in seconds (eg. 60*60*2 = 2 hours)
        print("Created a sine wave with %s second period" % wave_lenght)
        diagnostic_array = np.arange(0, 1, 1. / length)
        diagnostic_array = np.cos(2 * np.pi * temporal_window / wave_lenght * diagnostic_array)
        data = diagnostic_array
    a = np.abs(fft.rfft(data))
    a[0] = 0
    xt = np.linspace(0.0, temporal_window, a.size)
    if debug:
        index_value = np.argmax(a)
        while abs(index_value - 12) != 1:
            index_value = calc_periodicity(data, suggest_value + 2000, True, tryCount + 1)
        print("calculate suggest value is " % suggest_value)
        print("Actual index is" % np.argmax(a))
    print("Peak found at %s second period" % int(xt[np.argmax(a)]))
    # plt.subplot(211)
    # plt.plot(xt, a)
    # plt.subplot(212)
    # plt.plot(np.linspace(0, temporal_window, data.size), data)
    # plt.show()
    return int(xt[np.argmax(a)])


def periodic_prediction(period, data, code, type, count=1):
    print('---------- start periodic_prediction ----------')
    today = datetime.now().strftime(constant.date_format)
    new_period_value = list()
    predict_result = {
        "periodic": period,  # 周期
        "code": code,  # 股票代码
        "date": today,
        "periodid_type": type,
        "new_predict_value": new_period_value
    }
    weekday = datetime.now().weekday()

    for i in range(count):
        if weekday == 4 or weekday == 5 or weekday == 6:
            i = (7 - weekday) + i
        cal_periodic(data, i, new_period_value, type)
    return predict_result


def periodic_date(count):
    today = datetime.now()
    today = today + timedelta(days=count)
    return today.strftime(constant.date_format)


def cal_periodic(data, count, new_period_value, type):
    total_size = data.get_size(type)
    cur_periodic_value = total_size % period
    old_period_value = list()
    start_index = cur_periodic_value + count
    while start_index < total_size:
        temp_period_old_value = {}
        temp_period_old_value['price'] = data.get_price_array(type)[start_index]
        temp_period_old_value['date'] = data.get_date_array(type)[start_index]
        old_period_value.append(temp_period_old_value)
        start_index = start_index + period
    if len(old_period_value) == 1:
        temp_period_value = {
            "date": periodic_date(count),
            "price": np.average(old_period_value),
            "old_period": old_period_value
        }
        new_period_value.append(temp_period_value)
    else:
        first_value = 0
        for old_value in old_period_value:
            if first_value == 0:
                first_value = old_value['price']
            elif abs(first_value - old_value['price']) / first_value > 0.1:
                print('error big distance value ' % (abs(first_value - old_value['price']) / first_value))
        price = list()
        for old_price in old_period_value:
            price.append(old_price['price'])
        temp_period_value = {
            "date": periodic_date(count),
            "price": np.average(price),
            "old_periodix": old_period_value
        }
        new_period_value.append(temp_period_value)


dao = mongtest.StockDao()
stock_data = mongtest.StockDao.get_stock_array(dao, constant.db_database, constant.db_tushare_collection)
# #  init value 42014
period = calc_periodicity(stock_data.get_price_array(constant.type_open), 46014)
document = periodic_prediction(period, stock_data, constant.stock_code, constant.type_open,3)
dao.insert_predict_value(constant.db_database,constant.db_forecast_collection,document)
print(document)


period = calc_periodicity(stock_data.get_price_array(constant.type_high), 46014)
document = periodic_prediction(period, stock_data, constant.stock_code, constant.type_high,3)
dao.insert_predict_value(constant.db_database,constant.db_forecast_collection,document)
print(document)


period = calc_periodicity(stock_data.get_price_array(constant.type_three), 46014)
document = periodic_prediction(period, stock_data, constant.stock_code, constant.type_three,3)
dao.insert_predict_value(constant.db_database,constant.db_forecast_collection,document)
print(document)



