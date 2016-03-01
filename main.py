import bs4
import urllib.request
import urllib.response
import json

lanacion = ("La Nacion", "http://contenidos.lanacion.com.ar/json/dolar?callback=jsonpCallback")
preciodolar = ("Precio Dolar", "http://www.preciodolar.com.ar/")


data = str(urllib.request.urlopen(lanacion[1]).read())
dict = json.loads(data[data.find("{"):data.find("}")+1])

print(lanacion[0])
print("="*len(lanacion[0]))
print("Fecha:", dict["Date"])
print("Compra:", dict["CasaCambioCompraValue"])
print("Venta:", dict["CasaCambioVentaValue"])

#----

data = str(urllib.request.urlopen(preciodolar[1]).read())
soup = bs4.BeautifulSoup(data, "html.parser")
values = soup.find_all("td", class_="Estilo4")
print("-"*50)

print(preciodolar[0])
print("="*len(preciodolar[0]))
print("Fecha:",)
print("Compra:", values[0].contents)
print("Venta:", values[1].contents)
