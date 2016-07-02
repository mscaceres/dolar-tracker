import collections
import datetime
import itertools
import logging
import dollar_tracker.persitence


log = logging.getLogger(__name__)


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
            self._points[date] = {source: price}
        self._max_points[date] = max(price, self._max_points.get(date, price))
        self._min_points[date] = min(price, self._min_points.get(date, price))
        self.update_avg_values(self._avg_points, self._points, date)
        self.update_day_variation(self._day_variations, self._avg_points, date)
        self.update_month_variation(self._month_variations, self._day_variations, date)

    def get_indicators_by_date(self, date):
        return self._avg_points.get(date, 0), self._day_variations.get(date, 0), self._month_variations.get(date, 0)

    def __len__(self):
        return len(self._points)

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
    def update_avg_values(avg_dict, source_dict, date):
        if date in source_dict:
            avg_value = sum(source_dict[date].values())/len(source_dict[date])
            avg_dict[date] = avg_value

    @staticmethod
    def find_previous_date(date, dates):
        try:
            return next(itertools.dropwhile(lambda x: x >= date, reversed(dates)))
        except StopIteration:
            return None

    @staticmethod
    def update_day_variation(variations_dict, source_dict, date):
        if len(source_dict) >= 2:
            day_before = PriceHistory.find_previous_date(date, source_dict.keys())
            variation = ((source_dict[date] - source_dict[day_before]) / source_dict[day_before]) * 100
            variations_dict[date] = variation

    @staticmethod
    def update_month_variation(month_variations, source_dict, date):
        if len(source_dict) >= 2:
            ldpm = PriceHistory.find_previous_date(datetime.date(date.year, date.month, 1), source_dict.keys())
            variation = sum(source_dict[day] for day in
                            itertools.takewhile(lambda x: x.month == date.month or x == ldpm,
                                                reversed(source_dict.keys())))
            month_variations[date.month] = variation


class DolarHistory:

    def __init__(self):
        self.buy_prices = PriceHistory("Compra")
        self.sell_prices = PriceHistory("Venta")

    @classmethod
    def from_pickle(cls, path):
        return dollar_tracker.persitence.pickled_context(cls, path)

    def add_point(self, source, dollar_point):
        log.info("Adding point from {}: {}".format(source, dollar_point))
        self.buy_prices.add_point(source, dollar_point.date, dollar_point.buy_price)
        self.sell_prices.add_point(source, dollar_point.date, dollar_point.sell_price)

    def get_buy_indicators_by_date(self, date):
        return self.buy_prices.get_indicators_by_date(date)

    def get_sell_indicators_by_date(self, date):
        return self.sell_prices.get_indicators_by_date(date)

    def get_indicators_by_date(self, date=None):
        if date is None:
            date = datetime.date.today()
        return self.get_buy_indicators_by_date(date), self.get_sell_indicators_by_date(date)
