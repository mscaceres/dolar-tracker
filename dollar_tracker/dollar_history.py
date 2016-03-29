import collections
import datetime
import itertools


class PriceHistory:
    def __init__(self, name):
        self.name = name
        self._points = collections.defaultdict(list)
        self._max_points = collections.OrderedDict()
        self._min_points = collections.OrderedDict()
        self._avg_points = collections.OrderedDict()
        self._day_variations = collections.OrderedDict()
        self._month_variations = collections.OrderedDict()
        self._year_variations = collections.OrderedDict()

    def add_point(self, source, date, price):
        if date in self._points:
            self._points[date][source] = price
        else:
            self._points[date] = {source:price}
        self.update_limit_values(self._max_points, date, price, max)
        self.update_limit_values(self._min_points, date, price, min)
        self.update_avg_values(self._avg_points, self._points, date)
        self.update_day_variation(self._day_variations, self._avg_points, date)

    @property
    def max_points(self):
        return self._max_points.items()

    @property
    def min_points(self):
        return self._min_points.items()

    @property
    def avg_points(self):
        return self._avg_points.items()

    @property
    def day_variations(self):
        return self._day_variations.items()

    @property
    def month_variations(self):
        return self._month_variations.items()

    @property
    def year_variations(self):
        return self._year_variations.items()

    @staticmethod
    def update_limit_values(price_dict, date, price, op):
        if date in price_dict:
            price_dict[date] = op(price, price_dict[date])
        else:
            price_dict[date] = price

    @staticmethod
    def update_avg_values(avg_dict, source_dict, date):
        if date in source_dict:
            avg_value = sum(source_dict[date].values())/len(source_dict[date])
            avg_dict[date] = avg_value

    @staticmethod
    def find_previous_date(date, dates):
        return next(itertools.dropwhile(lambda x: x >= date, reversed(dates)))

    @staticmethod
    def update_day_variation(variations_dict, source_dict, date):
        if len(source_dict) >= 2:
            day_before = PriceHistory.find_previous_date(date, source_dict.keys())
            variation = ((source_dict[date] - source_dict[day_before]) / source_dict[day_before]) * 100
            variations_dict[date] = variation

    @staticmethod
    def update_month_variation(self):
        pass


class DolarHistory:

    def __init__(self):
        self.buy_prices = PriceHistory("Compra")
        self.sell_prices = PriceHistory("Venta")

    def add_point(self, source, dolar_point):
        self.buy_prices.add_point(source, dolar_point.date, dolar_point.buy_price)
        self.sell_prices.add_point(source, dolar_point.date, dolar_point.sell_price)