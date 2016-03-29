import pytest
import datetime
from dollar_tracker import plot
from dollar_tracker import scraping
from dollar_tracker import persitence
from dollar_tracker import dollar_history

DATE1 = datetime.date(2016, 5, 12)
DATE2 = datetime.date(2016, 5, 13)
DATE3 = datetime.date(2016, 5, 14)
DATE4 = datetime.date(2016, 5, 15)
DATE5 = datetime.date(2016, 5, 16)

@pytest.fixture
def history():
    history = dollar_history.DolarHistory()

    history.add_point("source1", scraping.DolarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", scraping.DolarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    history.add_point("source1", scraping.DolarPoint(date=DATE2, buy_price=12.53, sell_price=15.30))
    history.add_point("source2", scraping.DolarPoint(date=DATE2, buy_price=12.55, sell_price=15.02))
    history.add_point("source1", scraping.DolarPoint(date=DATE3, buy_price=12.59, sell_price=15.50))
    history.add_point("source2", scraping.DolarPoint(date=DATE3, buy_price=12.57, sell_price=15.03))
    return history


@pytest.fixture
def history2():
    history = dollar_history.DolarHistory()

    history.add_point("source1", scraping.DolarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", scraping.DolarPoint(date=DATE1, buy_price=12.20, sell_price=15.40))
    history.add_point("source1", scraping.DolarPoint(date=DATE2, buy_price=12.79, sell_price=15.30))
    history.add_point("source2", scraping.DolarPoint(date=DATE2, buy_price=12.30, sell_price=15.80))
    history.add_point("source1", scraping.DolarPoint(date=DATE3, buy_price=13, sell_price=13))
    history.add_point("source2", scraping.DolarPoint(date=DATE3, buy_price=12.57, sell_price=13.50))
    history.add_point("source1", scraping.DolarPoint(date=DATE4, buy_price=13, sell_price=13))
    history.add_point("source2", scraping.DolarPoint(date=DATE4, buy_price=12.57, sell_price=13.50))
    history.add_point("source1", scraping.DolarPoint(date=DATE5, buy_price=13, sell_price=13))
    history.add_point("source2", scraping.DolarPoint(date=DATE5, buy_price=12.57, sell_price=13.50))
    return history


# I have to change this test to use streams instead of paths
def test_save_history(history):
    persitence.save_history(history, r"test.pkl")
    other = persitence.load_history(r"test.pkl")
    assert (len(other.sell_prices._points.keys()) == 3)
    assert (len(other.buy_prices._points.keys()) == 3)
    assert (len(other.sell_prices._points[DATE1].keys()) == 2)


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


def test_get_scrap_functions():
    fnts = scraping.get_scrap_functions()
    assert (len(fnts) == 2)
    assert not fnts[0][0].startswith("scrap_")


def test_make_dashboard(history2):
    plot.make_dolar_dashboard(history2)


def test_variations(history):
    assert(len(history.buy_prices.day_variations) == len(history.buy_prices.avg_points)-1)


def test_find_previous_date():
    date = dollar_history.PriceHistory.find_previous_date(DATE3, [DATE1, DATE2, DATE3, DATE4, DATE5])
    assert date == DATE2

def test_find_previous_date2():
    date = dollar_history.PriceHistory.find_previous_date(DATE5, [DATE1, DATE2, DATE3, DATE4, DATE5])
    assert date == DATE4

