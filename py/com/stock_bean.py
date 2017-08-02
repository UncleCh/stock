class stock:
    __prices_dict = {}

    def setdate(self, price_array, date_array, percent_array, type):
        self.__prices_dict['date_array'] = date_array
        self.__prices_dict['percent_array'] = percent_array
        self.__prices_dict[type] = price_array

    def add_price_data(self,price_array,type):
        self.__prices_dict[type] = price_array

    def get_price_array(self, type):
        return self.__prices_dict.get(type)

    def get_date_array(self):
        return self.__prices_dict.get("date_array")

    def get_percent_array(self):
        return self.__prices_dict.get('percent_array')

    def get_size(self):
        return len(self.get_date_array())
