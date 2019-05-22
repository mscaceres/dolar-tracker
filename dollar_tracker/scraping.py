from abc import ABC, abstractmethod
import collections
import datetime
import urllib
import bs4
import logging

log = logging.getLogger(__name__)

DollarPoint = collections.namedtuple("DollarPoint", "date, buy_price, sell_price")


def scrapped_dolar_points():
    for source, scrap_class in DolarScrapper.SCRAPPERS.items():
        try:
            yield (source, scrap_class().scrap())
        except urllib.error.HTTPError as e:
            log.warn("{} can not be reached, {}".format(source, e))

def log_prices(source, date, buy_price, sell_price):
    log.info("""
        ** {0} **
        Fecha: {1}
        Compra: {2}
        Venta: {3}""".format(source, date, buy_price, sell_price))


class DolarScrapper(ABC):
    SCRAPPERS = None

    def __init_subclass__(cls):
        cls.SCRAPPERS[cls.source] = cls

    def scrap(self):
        date, buy_price, sell_price = self.scrap_source(self)
        return DollarPoint(date, buy_price, sell_price)

    @abstractmethod
    def scrap_source(self):
        raise NotImplemented

    @property
    def source(self):
        return self.__class__.__name__.replace('_', ' ').lower()


class La_Nacion(DolarScrapper):

    def scrap_source(self):
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
        return date, buy_price, sell_price


class Precio_Dolar(DolarScrapper):

    def scrap_source(self):
        url = "http://www.preciodolar.com.ar/"
        data = str(urllib.request.urlopen(url).read())
        soup = bs4.BeautifulSoup(data, "html.parser")
        values = soup.find_all("td", class_="Estilo4")
        buy_price = float(values[0].contents[0])
        sell_price = float(values[1].contents[0])
        date = datetime.date.today()
        log_prices("Precio Dolar", date, buy_price, sell_price)
        return date, buy_price, sell_price


class Ambito(DolarScrapper):

    def scrap_source():
        url = "http://www.ambito.com/economia/mercados/monedas/dolar/"
        data = str(urllib.request.urlopen(url).read())
        soup = bs4.BeautifulSoup(data, "html.parser")
        # values = soup.find_all("div", class_="ultimo")
        buy_price = float(soup.select_one(".columna1 .ultimo big").contents[0].replace(",", "."))
        sell_price = float(soup.select_one(".columna1 .cierreAnterior big").contents[0].replace(",", "."))
        date = datetime.date.today()
        log_prices("Ambito Financiero", date, buy_price, sell_price)
        return date, buy_price, sell_price
