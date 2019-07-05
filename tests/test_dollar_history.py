from dollar_tracker.scrap.scrappers import Ambito
from tests.conftest import DATE1, DATE2, DATE3, DATE4, DATE5

from dollar_tracker.dollar_history import DollarHistory, PriceHistory

def test_limit_values(history):
    assert (history.buy_prices._max_points[DATE1] == 12.51)
    assert (history.buy_prices._max_points[DATE2] == 12.55)
    assert (history.buy_prices._max_points[DATE3] == 12.59)

    assert (history.buy_prices._min_points[DATE1] == 12.50)
    assert (history.buy_prices._min_points[DATE2] == 12.53)
    assert (history.buy_prices._min_points[DATE3] == 12.57)


def test_avg_values(history):
    assert history.sell_prices._avg_points[DATE1] == (15+15.01)/2
    assert history.sell_prices._avg_points[DATE2] == (15.30+15.02)/2
    assert history.sell_prices._avg_points[DATE3] == (15.50+15.03)/2


def test_points_saved(history_one_date):
    assert len(history_one_date.buy_prices._points[DATE1]['source1']) == 3
    assert len(history_one_date.sell_prices._points[DATE1]['source1']) == 3
    assert len(history_one_date.buy_prices._points[DATE1]['source2']) == 4
    assert len(history_one_date.sell_prices._points[DATE1]['source2']) == 4
    assert "{:.2f}".format(history_one_date.buy_prices._avg_points[DATE1]) == "13.79"


def test_avg_with_one_point(history_one_date_one_point):
    assert "{:.2f}".format(history_one_date_one_point.buy_prices._avg_points[DATE1]) == "12.50"
    assert "{:.2f}".format(history_one_date_one_point.sell_prices._avg_points[DATE1]) == "15.00"
    assert history_one_date_one_point.avg_values_for(DATE1) == (12.50,15.00)


def test_avg_no_points():
    history = DollarHistory()
    assert history.avg_values_for(DATE1) == (None, None)


def test_points_for_date_no_points():
    single_price = PriceHistory('Compra')
    assert single_price.points_for_date(DATE1) == (None, None ,None)

def test_last_value_no_points():
    single_price = PriceHistory('Compra')
    assert single_price.last_value_for_date(DATE1) == None


def test_last_value_for_date():
    single_price = PriceHistory('Compra')
    single_price.add_point('source1', DATE1, 12)
    single_price.add_point('source2', DATE1, 13)
    single_price.add_point('source3', DATE1, 14)
    single_price.add_point('source1', DATE1, 15)
    single_price.add_point('source2', DATE1, 16)
    single_price.add_point('source3', DATE1, 17)
    assert single_price.last_value_for_date(DATE1) == 17


def test_points_for_date():
    single_price = PriceHistory('Compra')
    single_price.add_point('source1', DATE1, 12)
    single_price.add_point('source2', DATE1, 13)
    single_price.add_point('source3', DATE1, 14)
    single_price.add_point('source1', DATE1, 15)
    single_price.add_point('source2', DATE1, 16)
    single_price.add_point('source3', DATE1, 17)
    assert single_price.points_for_date(DATE1) == (12, 14.5 ,17)


def test_history_to_dict(history):
    data = history.to_dict()
    assert 'Compra' in data
    assert 'Venta' in data
    for price in (data['Compra'], data['Venta']):
        for field in ('name', 'all_points', 'max_points', 'min_points', 'avg_points'):
            assert field in price


def test_history_from_dict(history):
    data = history.to_dict()
    from_data_history = DollarHistory.from_dict(data)
    attributes = ('_points', '_max_points', '_min_points', '_avg_points')
    for attribute in attributes:
        for price_attr in ('buy_prices', 'sell_prices'):
           assert (getattr(getattr(from_data_history, price_attr), attribute) ==
                   getattr(getattr(history, price_attr), attribute))
