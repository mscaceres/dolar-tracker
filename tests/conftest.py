import pytest
import datetime

from dollar_tracker.dollar_history import DollarHistory
from dollar_tracker.scrap.scrappers import DollarPoint, Ambito

DATE1 = datetime.date(2016, 5, 12)
DATE2 = datetime.date(2016, 5, 13)
DATE3 = datetime.date(2016, 5, 14)
DATE4 = datetime.date(2016, 5, 15)
DATE5 = datetime.date(2016, 5, 16)

@pytest.fixture
def history():
    history = DollarHistory()

    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    history.add_point("source1", DollarPoint(date=DATE2, buy_price=12.53, sell_price=15.30))
    history.add_point("source2", DollarPoint(date=DATE2, buy_price=12.55, sell_price=15.02))
    history.add_point("source1", DollarPoint(date=DATE3, buy_price=12.59, sell_price=15.50))
    history.add_point("source2", DollarPoint(date=DATE3, buy_price=12.57, sell_price=15.03))
    return history


@pytest.fixture
def history_one_date():
    history = DollarHistory()

    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    history.add_point("source1", DollarPoint(date=DATE1, buy_price=13.50, sell_price=15))
    history.add_point("source1", DollarPoint(date=DATE1, buy_price=14.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=12.51, sell_price=15.01))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=13.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=14.50, sell_price=15))
    history.add_point("source2", DollarPoint(date=DATE1, buy_price=15.50, sell_price=15))
    return history

@pytest.fixture
def history_one_date_one_point():
    history = DollarHistory()
    history.add_point("source1", DollarPoint(date=DATE1, buy_price=12.50, sell_price=15))
    return history
