import xml.etree.ElementTree as ET
import requests
import sys
#from functools import lru_cache




# Для загрузки данных напрямую, без локального сохранения.

url_n = "http://alitair.1gb.ru/Intim_Ali_allfids_2.xml"
url_p = "http://stripmag.ru/datafeed/p5s_full_stock.xml"

splitter = lambda x: x.split("/")[2]
try:
    response = requests.get(url_n, headers={'User-Agent': 'XYZ/3.0'})
    if response.status_code == 200:
        print(f"Подключение успешно {splitter(url_n)}")
        tree_fed = ET.fromstring(response.content)
except ConnectionError:
    print(f"Сервер {url_n} не отвечает")
    sys.exit("Повторите попытку позднее")

try:
    response = requests.get(url_p, headers={'User-Agent': 'XYZ/3.0'})
    if response.status_code == 200:
        print(f"Подключение успешно {splitter(url_p)}")
        tree_stock = ET.fromstring(response.content)
except ConnectionError:
    print(f"Сервер {url_p} не отвечает")
    sys.exit("Повторите попытку позднее")

#Для локальной загрузки
#tree_fed = ET.parse('Intim_Ali_allfids_2.xml')  # Наш фид
#root  = tree_fed.getroot()
#tree_stock = ET.parse('p5s_full_stock.xml')  # файл поставщика
#root_stock  = tree_stock.getroot()


def get_stats(item):
    RetailPrice = item.find("price").get("RetailPrice")
    BaseRetailPrice = item.find("price").get("BaseRetailPrice")
    WholePrice = item.find("price").get("WholePrice")
    BaseWholePrice = item.find("price").get("BaseWholePrice")
    return RetailPrice,BaseRetailPrice,WholePrice,BaseWholePrice

Stock_Dict  = {}  # Словарь с ценами от поставщика
for item in tree_stock.findall("product"):
    id = item.get("prodID")
    amount = item.find("assortiment").find("assort").get("sklad")
    RP,BRP,WP,BWP = get_stats(item)
    Stock_Dict[id] = {}
    Stock_Dict[id]["amount"] = amount
    Stock_Dict[id]["RetailPrice"] = RP
    Stock_Dict[id]["BaseRetailPrice"] =  BRP
    Stock_Dict[id]["WholePrice"] = WP
    Stock_Dict[id]["BaseWholePrice"] = BWP

#Заменяем на акутальные цены
for item in tree_fed[0][1].findall('offer'):
    id = item.get("id")  # Айди товара
    if id in Stock_Dict:
        item.find("quantity").text = str(Stock_Dict.get(id)["amount"]) # Колличество товара
        item.find("price").set("RetailPrice",Stock_Dict[id]["RetailPrice"])
        item.find("price").set("BaseRetailPrice", Stock_Dict[id]["BaseRetailPrice"])
        item.find("price").set("WholePrice", Stock_Dict[id]["WholePrice"])
        item.find("price").set("BaseWholePrice", Stock_Dict[id]["BaseWholePrice"])


print("Cохраняю")
tree = ET.ElementTree(tree_fed)
tree.write("output.xml",encoding="utf-8",xml_declaration=True,short_empty_elements = False)
print("Запись в файл успешно")

