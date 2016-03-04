import pytest
import main
import datetime

DATE1 = datetime.date(2016, 5, 12)
DATE2 = datetime.date(2016, 5, 13)
DATE3 = datetime.date(2016, 5, 14)

@pytest.fixture
def history():
    history = main.DolarHistory()

    history.add_point("source1", main.DolarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", main.DolarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    history.add_point("source1", main.DolarPoint(date=DATE2, buy_price=12.53, sell_price=15.30))
    history.add_point("source2", main.DolarPoint(date=DATE2, buy_price=12.55, sell_price=15.02))
    history.add_point("source1", main.DolarPoint(date=DATE3, buy_price=12.59, sell_price=15.50))
    history.add_point("source2", main.DolarPoint(date=DATE3, buy_price=12.57, sell_price=15.03))
    return history


# I have to change this test to use streams instead of paths
def test_save_history(history):
    main.save_history(history, r"C:\gitrepos\dolar-tracker\test.pkl")
    other = main.load_history(r"C:\gitrepos\dolar-tracker\test.pkl")
    assert (len(other.points.keys()) == 2)
    assert (len(other.points["source2"]) == 3)

def test_limit_values(history):
    assert (history.max_buy_points[0] == (DATE1, 12.51))
    assert (history.max_buy_points[1] == (DATE2, 12.55))
    assert (history.max_buy_points[2] == (DATE3, 12.59))

    assert (history.min_buy_points[0] == (DATE1, 12.50))
    assert (history.min_buy_points[1] == (DATE2, 12.53))
    assert (history.min_buy_points[2] == (DATE3, 12.57))

def test_avg_values(history):
    assert (history.avg_sell_points[0] == (DATE1, (15+15.01)/2))
    assert (history.avg_sell_points[1] == (DATE2, (15.30+15.02)/2))
    assert (history.avg_sell_points[2] == (DATE3, (15.50+15.03)/2))


def test_get_scrap_functions():
    fnts = main.get_scrap_functions()
    assert (len(fnts) == 2)
