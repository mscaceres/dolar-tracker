import bs4
import urllib.request
import collections
import sys
import pickle
import plotly.offline
import plotly.graph_objs
import datetime

HISTORY_FILE = "./dolar_history.pkl"

DolarPoint = collections.namedtuple("DolarPoint", "date, buy_price, sell_price")


def scrap_la_nacion():
    import json
    url = "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback"
    json_response = str(urllib.request.urlopen(url).read())
    dict = json.loads(json_response[json_response.find("{"):json_response.find("}")+1])
    buy_price = float(dict["CasaCambioCompraValue"].replace(",", "."))
    sell_price = float(dict["CasaCambioVentaValue"].replace(",", "."))
    date = datetime.datetime.strptime(dict["Date"][:dict["Date"].find("T")], "%Y-%m-%d")
    print("La Nacion")
    print("Fecha:", date)
    print("Compra:", buy_price)
    print("Venta:", sell_price)

    return DolarPoint(date=date, buy_price=buy_price, sell_price=sell_price)


def scrap_precio_dolar():
    url = "http://www.preciodolar.com.ar/"
    data = str(urllib.request.urlopen(url))
    soup = bs4.BeautifulSoup(data, "html.parser")
    values = soup.find_all("td", class_="Estilo4")
    buy_price = float(values[0].contents[0])
    sell_price = float(values[1].contents[0])
    date = datetime.date.today()
    print("Precio Dolar")
    print("Fecha:", date)
    print("Compra:", buy_price)
    print("Venta:", sell_price)
    return DolarPoint(date=date, buy_price=buy_price, sell_price=sell_price)


def save_history(history, path):
    with open(path, 'wb') as output:
        pickle.dump(history, output)


def load_history(path):
    history_obj = None
    try:
        with open(path, 'rb') as input:
            history_obj = pickle.load(input)
    except IOError:
        history_obj = DolarHistory()
    return history_obj


def get_scrap_functions():
    """Look for scrap_<functions> in the current file"""
    return [v for k,v in globals().items() if k.startswith("scrap_") and callable(v)]


class DolarHistory:

    def __init__(self):
        self.points = collections.defaultdict(list)

        self.max_buy_points = []
        self.min_buy_points = []
        self.avg_buy_points = []
        self.buy_points = collections.defaultdict(list)

        self.max_sell_points = []
        self.min_sell_points = []
        self.avg_sell_points = []
        self.sell_points = collections.defaultdict(list)

    @staticmethod
    def update_limit_values(price_list, date, price, op):
        """update price_list with max/min between the latest element in the list and the provided values.
        It assumes price_list is sorted, so the last value is the latest by date"""
        try:
            last_date, last_value = price_list[-1]
            if date == last_date:
                price_list[-1] = (last_date, (op(last_value, price)))
            else:
                price_list.append((date, price))
        except IndexError:
            price_list.append((date, price))

    @staticmethod
    def update_avg_values(price_list, source_list, date):
        """Updates price_list with an avg value calculated from source_list values.
        source_list is a {source:[(date,price)] that is indexded with the provided date"""
        last_prices = []
        for source in source_list.keys():
            if date == source_list[source][-1][0]:
                last_prices.append(source_list[source][-1][1])
        last_avg_value = sum(last_prices)/len(last_prices)

        if len(price_list) and price_list[-1][0] == date:
            price_list[-1] = (date, last_avg_value)
        else:
            price_list.append((date, last_avg_value))

    def add_point(self, source, dolar_point):
        self.points[source].append(dolar_point)
        self.buy_points[source].append((dolar_point.date, dolar_point.buy_price))
        self.sell_points[source].append((dolar_point.date, dolar_point.sell_price))

        self.update_limit_values(self.max_buy_points, dolar_point.date, dolar_point.buy_price, max)
        self.update_limit_values(self.max_sell_points, dolar_point.date, dolar_point.sell_price, max)
        self.update_limit_values(self.min_buy_points, dolar_point.date, dolar_point.buy_price, min)
        self.update_limit_values(self.min_sell_points, dolar_point.date, dolar_point.sell_price, min)

        self.update_avg_values(self.avg_buy_points, self.buy_points, dolar_point.date)
        self.update_avg_values(self.avg_sell_points, self.sell_points, dolar_point.date)


    # I should separate chart code from the data...
    def plot(self):
        #for values in self.points["la_nacion"]:

        dates, buy_values, sell_values = zip(*self.points["la_nacion"])
        # buy_values = [point.buy_price for point in self.points["la_nacion"]]
        # sell_values = [point.sell_price for point in self.points["la_nacion"]]
        # dates = [point.date for point in self.points["la_nacion"]]
        buy_line = plotly.graph_objs.Scatter(x=dates,
                                             y=buy_values,
                                             mode="lines+markers",
                                             name="Precio Compra",
                                             )
        sell_line = plotly.graph_objs.Scatter(x=dates,
                                              y=sell_values,
                                              mode="lines+markers",
                                              name="Precio Venta")
        plotly.offline.plot([buy_line, sell_line])


def main():
    history = DolarHistory()
    history.add_point("la_nacion", scrap_la_nacion())
    history.plot()

# def main():
#      history = load_history(HISTORY_FILE)
#      scrap_functions = get_scrap_functions()
#      for scrap_page in scrap_functions:
#          history.add_point(scrap_page())
#      history.plot()
#     save_history(HISTORY_FILE)

if __name__ == "__main__":
    sys.exit(main())
