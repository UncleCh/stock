class stock:

    __prices_dict = {}

    def setdate(self,price_array,date_array,type):
        data_list = list()
        data_list.append(price_array)
        data_list.append(date_array)
        self.__prices_dict[type] =data_list

    def get_price_array(self,type):
        return self.__prices_dict.get(type)[0]

    def get_date_array(self,type):
        return self.__prices_dict.get(type)[1]

    def get_size(self,type):
        return len(self.get_price_array(type))
