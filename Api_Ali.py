import xml.etree.ElementTree as ET
import json
#import top.api



tree_fed = ET.parse('output.xml')  # Наш фид
root  = tree_fed.getroot()


items = {}
for i,item in enumerate(root[0][1].findall('offer')[:50]):
    id = item.get("id")  # Айди товара
    amount = item.find("quantity").text
    items[i] = {}
    items[i]["product_id"] = id
    items[i]["multiple_sku_update_list"] = [{}]
    items[i]["multiple_sku_update_list"][0]["inventory"] = amount
    items[i]["multiple_sku_update_list"][0]["sku_code"] = "123def"


with open("amount_data_file.json", "w") as write_file:
    json.dump(items, write_file,indent = 4)

print("Готово")

"""
req=top.api.AliexpressSolutionBatchProductInventoryUpdateRequest(url,port)
req.set_app_info(top.appinfo(appkey,secret))

req.mutiple_product_update_list=""
try:
	resp= req.getResponse(sessionkey)
	print(resp)
except Exception,e:
	print(e)

"""