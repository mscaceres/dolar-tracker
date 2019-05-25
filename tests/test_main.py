import pytest
import datetime
import collections
from dollar_tracker import dollar_history
from dollar_tracker.scrap.scrappers import DollarPoint, Ambito

DATE1 = datetime.date(2016, 5, 12)
DATE2 = datetime.date(2016, 5, 13)
DATE3 = datetime.date(2016, 5, 14)
DATE4 = datetime.date(2016, 5, 15)
DATE5 = datetime.date(2016, 5, 16)

@pytest.fixture
def history():
    history = dollar_history.DolarHistory()

    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    history.add_point("source1", DollarPoint(date=DATE2, buy_price=12.53, sell_price=15.30))
    history.add_point("source2", DollarPoint(date=DATE2, buy_price=12.55, sell_price=15.02))
    history.add_point("source1", DollarPoint(date=DATE3, buy_price=12.59, sell_price=15.50))
    history.add_point("source2", DollarPoint(date=DATE3, buy_price=12.57, sell_price=15.03))
    return history


@pytest.fixture
def one_history():
    history = dollar_history.DolarHistory()

    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    return history


@pytest.fixture
def history2():
    history = dollar_history.DolarHistory()

    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=12.20, sell_price=15.40))
    history.add_point("source1", DollarPoint(date=DATE2, buy_price=12.79, sell_price=15.30))
    history.add_point("source2", DollarPoint(date=DATE2, buy_price=12.30, sell_price=15.80))
    history.add_point("source1", DollarPoint(date=DATE3, buy_price=13, sell_price=13))
    history.add_point("source2", DollarPoint(date=DATE3, buy_price=12.57, sell_price=13.50))
    history.add_point("source1", DollarPoint(date=DATE4, buy_price=13, sell_price=13))
    history.add_point("source2", DollarPoint(date=DATE4, buy_price=12.57, sell_price=13.50))
    history.add_point("source1", DollarPoint(date=DATE5, buy_price=13, sell_price=13))
    history.add_point("source2", DollarPoint(date=DATE5, buy_price=12.57, sell_price=13.50))
    return history


def test_limit_values(history):
    assert (history.buy_prices._max_points[DATE1] == 12.51)
    assert (history.buy_prices._max_points[DATE2] == 12.55)
    assert (history.buy_prices._max_points[DATE3] == 12.59)

    assert (history.buy_prices._min_points[DATE1] == 12.50)
    assert (history.buy_prices._min_points[DATE2] == 12.53)
    assert (history.buy_prices._min_points[DATE3] == 12.57)


def test_avg_values(history):
    assert (history.sell_prices._avg_points[DATE1] == (15+15.01)/2)
    assert (history.sell_prices._avg_points[DATE2] == (15.30+15.02)/2)
    assert (history.sell_prices._avg_points[DATE3] == (15.50+15.03)/2)


def test_scrap_ambito():
    point = Ambito().scrap()
    assert point is not None
    assert type(point.buy_price) is float
    assert type(point.sell_price) is float
