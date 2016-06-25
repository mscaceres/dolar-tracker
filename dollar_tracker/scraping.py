import collections
import datetime
import urllib
import bs4
import logging

log = logging.getLogger(__name__)

DollarPoint = collections.namedtuple("DollarPoint", "date, buy_price, sell_price")


def get_scrap_functions():
    """Look for funtions with the name 'scrap_<source>' in the current file.
    It return the pair (<source>, function)"""
    return [(k.replace("scrap_", ""), v) for k, v in globals().items() if k.startswith("scrap_") and callable(v)]


def log_prices(source, date, buy_price, sell_price):
    log.info("""
        ** {0} **
        Fecha: {1}
        Compra: {2}
        Venta: {3}""".format(source, date, buy_price, sell_price))

def scrap_la_nacion():
    import json
    url = "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback"
    json_response = str(urllib.request.urlopen(url).read())
    dict = json.loads(json_response[json_response.find("{"):json_response.find("}")+1])
    buy_price = float(dict["CasaCambioCompraValue"].replace(",", "."))
    sell_price = float(dict["CasaCambioVentaValue"].replace(",", "."))
    #the returned json does not look that is updating the date...
    #datetime.datetime.strptime(dict["Date"][:dict["Date"].find("T")], "%Y-%m-%d")
    date = datetime.date.today()
    log_prices("La Nacion", date, buy_price, sell_price)
    return DollarPoint(date=date, buy_price=buy_price, sell_price=sell_price)


def scrap_precio_dolar():
    url = "http://www.preciodolar.com.ar/"
    data = str(urllib.request.urlopen(url).read())
    soup = bs4.BeautifulSoup(data, "html.parser")
    values = soup.find_all("td", class_="Estilo4")
    buy_price = float(values[0].contents[0])
    sell_price = float(values[1].contents[0])
    date = datetime.date.today()
    log_prices("Precio Dolar", date, buy_price, sell_price)
    return DollarPoint(date=date, buy_price=buy_price, sell_price=sell_price)


def scrap_ambito():
    url = "http://www.ambito.com/economia/mercados/monedas/dolar/"
    data = str(urllib.request.urlopen(url).read())
    soup = bs4.BeautifulSoup(data, "html.parser")
    # values = soup.find_all("div", class_="ultimo")
    buy_price = float(soup.select_one(".columna1 .ultimo big").contents[0].replace(",", "."))
    sell_price = float(soup.select_one(".columna1 .cierreAnterior big").contents[0].replace(",", "."))
    date = datetime.date.today()
    log_prices("Ambito Financiero", date, buy_price, sell_price)
    return DollarPoint(date=date, buy_price=buy_price, sell_price=sell_price)
