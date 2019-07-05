import collections
import datetime
import itertools
import logging
import dollar_tracker.persitence


log = logging.getLogger(__name__)

def collections_default_list():
    return collections.defaultdict(list)

class PriceHistory:
    def __init__(self, name):
        self.name = name
        self._points = collections.defaultdict(collections_default_list)
        self._max_points = collections.OrderedDict()
        self._min_points = collections.OrderedDict()
        self._avg_points = collections.OrderedDict()

    def add_point(self, source, date, price):
        self._points[date][source].append(price)
        self._max_points[date] = max(price, self._max_points.get(date, price))
        self._min_points[date] = min(price, self._min_points.get(date, price))
        self.update_avg_value(date, price)

    def points_per_day(self, date):
        """Count the number of samples taken in a given day"""
        return sum(len(self._points[date][source])
                   for source in self._points[date])

    @property
    def max_points(self):
        return self._max_points.items()

    @property
    def min_points(self):
        return self._min_points.items()

    @property
    def avg_points(self):
        return self._avg_points.items()

    def update_avg_value(self, date, price):
        current_avg = self._avg_points.get(date, 0)
        self._avg_points[date] = current_avg + (price - current_avg) / self.points_per_day(date)

    def avg_variation_btw(self, date_from, date_to):
        if self.are_btw_dates_valid(date_from, date_to):
            return ((self._avg_points[date_to] - self._avg_points[date_from]) / self._avg_points[date_from]) * 100
        else:
            return None

    def max_variation_btw(self, date_from, date_to):
        if self.are_btw_dates_valid(date_from, date_to):
            return ((self._max_points[date_to] - self._max_points[date_from]) / self._max_points[date_from]) * 100
        else:
            return None


    def are_btw_dates_valid(self, date_from, date_to):
        return (len(self._avg_points) >= 2
                and date_from <= date_to
                and date_from in self._avg_points
                and date_to in self._avg_points
               )

    def points_for_date(self, date):
        """Returns the min, avg and max value for a given date"""
        return (self._min_points.get(date, None),
                self.avg_value_for_date(date),
                self._max_points.get(date, None))

    def avg_value_for_date(self, date):
        return self._avg_points.get(date, None)

    def last_value_for_date(self, date):
        """Returns the max last value added
        Given we might have many sources, take the last value added to each source and take the max value
        """
        sources = self._points.get(date, {})
        if sources:
            return max(itertools.chain.from_iterable(sources.values()))
        else:
            return None

    def to_dict(self):
        return {'name': self.name,
                'all_points': self._points,
                'max_points': self._max_points,
                'min_points': self._min_points,
                'avg_points': self._avg_points
               }

    @classmethod
    def from_dict(cls, data_dict):
        obj = cls(data_dict['name'])
        obj._points = data_dict['all_points']
        obj._max_points = data_dict['max_points']
        obj._min_points = data_dict['min_points']
        obj._avg_points = data_dict['avg_points']
        return obj


class DollarHistory:

    def __init__(self):
        self.buy_prices = PriceHistory("Compra")
        self.sell_prices = PriceHistory("Venta")

    @classmethod
    def pkl_context(cls, path):
        return dollar_tracker.persitence.pickled_context(cls, path)

    @classmethod
    def json_context(cls, path):
        return dollar_tracker.persitence.json_context(cls, path)

    @classmethod
    def from_dict(cls, data_dict):
        obj = cls()
        obj.buy_prices = PriceHistory.from_dict(data_dict[obj.buy_prices.name])
        obj.sell_prices = PriceHistory.from_dict(data_dict[obj.sell_prices.name])
        return obj

    def to_dict(self):
        return {self.buy_prices.name: self.buy_prices.to_dict(),
                self.sell_prices.name: self.sell_prices.to_dict(),
               }

    def add_point(self, source, dollar_point):
        log.info("Adding point from {}: {}".format(source, dollar_point))
        self.buy_prices.add_point(source, dollar_point.date, dollar_point.buy_price)
        self.sell_prices.add_point(source, dollar_point.date, dollar_point.sell_price)

    def avg_values_for(self, date):
        """Returns the avg price (buy, selll) for a given date"""
        buy_avg = self.buy_prices.avg_value_for_date(date)
        sell_avg = self.sell_prices.avg_value_for_date(date)
        return (buy_avg, sell_avg)

    def last_values_for(self, date):
        """Returns tha maximun of the last samples taken"""
        buy_last = self.buy_prices.last_value_for_date(date)
        sell_last = self.sell_prices.last_value_for_date(date)
        return (buy_last, sell_last)

    def points_for(self, date):
        """Returns the min, avg, max for a given date"""
        buy_points = self.buy_prices.points_for_date(date)
        sell_points = self.sell_prices.points_for_date(date)
        return (buy_points, sell_points)

