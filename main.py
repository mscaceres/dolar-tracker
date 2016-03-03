import bs4
import urllib.request
import collections
import sys
import pickle
import plotly.offline
import plotly.graph_objs

HISTORY_FILE = "./dolar_history.pkl"


def scrap_la_nacion():
    import json
    url = "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback"
    json_response = str(urllib.request.urlopen(url).read())
    dict = json.loads(json_response[json_response.find("{"):json_response.find("}")+1])
    print("La Nacion")
    print("Fecha:", dict["Date"])
    print("Compra:", dict["CasaCambioCompraValue"])
    print("Venta:", dict["CasaCambioVentaValue"])
    return Dolar_Point(date=dict["Date"], buy_price=dict["CasaCambioCompraValue"], sell_price=dict["CasaCambioVentaValue"])


def scrap_precio_dolar():
    data = str(urllib.request.urlopen(preciodolar[1]).read())
    soup = bs4.BeautifulSoup(data, "html.parser")
    values = soup.find_all("td", class_="Estilo4")
    print("Fecha:",)
    print("Compra:", values[0].contents)
    print("Venta:", values[1].contents)
    return Dolar_Point(date=None, buy_price=values[0].contents[0], sell_price=values[1].contents[0])


def save_history(history):
    with open(HISTORY_FILE, 'wb') as output:
        pickle.dump(history, output)


def load_history():
    history_obj = None
    try:
        with open(HISTORY_FILE, 'rb') as input:
            history_obj = pickle.load(input)
    except IOError:
        history_obj = DolarHistory()
    return history_obj


def get_scrap_functions():
    pass


class DolarHistory:

    def __init__(self):
        self.points = collections.defaultdict(list)
        self.latest_buy_value = None
        self.latest_sell_value = None

    def add_point(self, source, dolar_point):
        self.points[source].append(dolar_point)

    # I should separate chart code from the data...
    def plot(self):
        #for values in self.points["la_nacion"]:
        buy_values = [point.buy_price for point in self.points["la_nacion"]]
        sell_values = [point.sell_price for point in self.points["la_nacion"]]
        dates = [point.date for point in self.points["la_nacion"]]
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
#      history = load_history()
#      scrap_functions = get_scrap_functions()
#      for scrap_page in scrap_functions:
#          history.add_point(scrap_page())
#      history.plot()
#     save_history(history)

if __name__ == "__main__":
    sys.exit(main())
