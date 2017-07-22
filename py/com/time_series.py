import numpy as np
import numpy.fft as fft
from tutorial import mongtest
from datetime import datetime
from tutorial import constant
from datetime import timedelta

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
            tryCount = tryCount + 1
            suggest_value = suggest_value + 2000
            index_value = calc_periodicity(data, suggest_value, True, tryCount)
        print("calculate suggest value is " % suggest_value)
        print("Actual index is" % np.argmax(a))
    print("Peak found at %s second period" % int(xt[np.argmax(a)]))
    # plt.subplot(211)
    # plt.plot(xt, a)
    # plt.subplot(212)
    # plt.plot(np.linspace(0, temporal_window, data.size), data)
    # plt.show()
    return int(xt[np.argmax(a)])


def periodic_prediction(period, data, code, count=1):
    print('---------- start periodic_prediction ----------')
    today = datetime.now().strftime("%Y-%m-%d")
    predict_result = {
        "periodic": period,  # 周期
        "code": code,  # 股票代码
        "date": today,
        "periodid_type": 1
    }
    total_size = data.size
    cur_periodic_value = total_size % period
    old_period_value = list()
    start_index = cur_periodic_value
    while start_index < total_size:
        old_period_value.append(data[start_index])
        start_index = start_index + period
    predict_result['old_periodix'] = old_period_value
    if len(old_period_value) == 1:
        return old_period_value[0]
    else:
        first_value = 0
        for old_value in old_period_value:
            if first_value == 0:
                first_value = old_value
            elif abs(first_value - old_value) / first_value > 0.1:
                print('error big distance value ' % abs(first_value - old_value) / first_value)
        temp_period_value = {}
        predict_result['new_predict_value'] = np.average(old_period_value)
        return predict_result


def periodic_date(count):
    today = datetime.now().strftime("%Y-%m-%d")
    if count == 1:
        return today
    else:
        new_day = today + timedelta(days=count -1)
        week = new_day.weekday()



dao = mongtest.StockDao()
stock_data = mongtest.StockDao.get_stock_array(dao)
#  init value 42014
period = calc_periodicity(stock_data, 46014)
result = periodic_prediction(period, stock_data,constant.stock_code)
print(result)
