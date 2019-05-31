from abc import ABC, abstractmethod
import collections
import logging
import datetime
import urllib
import bs4

log = logging.getLogger(__name__)

DollarPoint = collections.namedtuple("DollarPoint", "date, buy_price, sell_price")

class DollarScrapper(ABC):
    SCRAPPERS = {}
    NAME = None
    URL = None

    def __init_subclass__(cls):
        cls.SCRAPPERS[cls.__name__] = cls

    def scrap(self):
        date, buy_price, sell_price = self.scrap_source()
        self.log_prices(date, buy_price, sell_price)
        return DollarPoint(date, buy_price, sell_price)

    @abstractmethod
    def scrap_source(self):
        raise NotImplemented

    @property
    def source(self):
        return self.__class__.scrapper_name()

    def log_prices(self, date, buy_price, sell_price):
        log.info("""
            ** {0} **
            Fecha: {1}
            Compra: {2}
            Venta: {3}""".format(self.source, date, buy_price, sell_price))

    @classmethod
    def scrappers(cls):
        return cls.SCRAPPERS.values()

    @classmethod
    def scrapper_name(cls):
        return cls.NAME or cls.__name__.replace('_', ' ').lower()

#These could go in their own file under this package
class La_Nacion(DollarScrapper):

    NAME = 'la nacion'
    URL = "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback"

    def scrap_source(self):
        import json
        json_response = str(urllib.request.urlopen(self.URL).read())
        dict = json.loads(json_response[json_response.find("{"):json_response.find("}")+1])
        buy_price = float(dict["CasaCambioCompraValue"].replace(",", "."))
        sell_price = float(dict["CasaCambioVentaValue"].replace(",", "."))
        #the returned json does not look that is updating the date...
        #datetime.datetime.strptime(dict["Date"][:dict["Date"].find("T")], "%Y-%m-%d")
        date = datetime.date.today()
        return date, buy_price, sell_price


class Precio_Dolar(DollarScrapper):
    NAME = 'precio dolar'
    URL = "http://www.preciodolar.com.ar/"

    def scrap_source(self):
        data = str(urllib.request.urlopen(self.URL).read())
        soup = bs4.BeautifulSoup(data, "html.parser")
        values = soup.find_all("td", class_="Estilo4")
        buy_price = float(values[0].contents[0])
        sell_price = float(values[1].contents[0])
        date = datetime.date.today()
        return date, buy_price, sell_price


class Ambito(DollarScrapper):
    NAME = 'ambito'
    URL = "http://www.ambito.com/economia/mercados/monedas/dolar/"

    def scrap_source(self):
        data = str(urllib.request.urlopen(url).read())
        soup = bs4.BeautifulSoup(data, "html.parser")
        # values = soup.find_all("div", class_="ultimo")
        buy_price = float(soup.select_one(".columna1 .ultimo big").contents[0].replace(",", "."))
        sell_price = float(soup.select_one(".columna1 .cierreAnterior big").contents[0].replace(",", "."))
        date = datetime.date.today()

