from bs4 import BeautifulSoup
import re
import requests
import csv
import pyfiglet

Name = pyfiglet.figlet_format("Mazen Tayseer")
print(Name)

search = input("Search a product: ")

url = f"https://www.newegg.com/p/pl?d={search}&N=4131"
html = requests.get(url).text
doc = BeautifulSoup(html, "html.parser")

pages = int(doc.find(class_="list-tool-pagination-text").text.split("/", 1)[1])
items_found = {}
i = 0

for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?d={search}&N=4131&page={page}"
    html = requests.get(url).text
    doc = BeautifulSoup(html, "html.parser")
    div = doc.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    items = div.find_all(text=re.compile(search))
    for item in items:
        parent = item.parent
        link = None
        if parent.name != "a":
            continue

        link = parent["href"]
        next_parent = parent.parent.parent

        try:
            price = next_parent.find(
                class_="price-current").strong.text.replace(",", "")
            items_found[item] = {
                "price": int(price),
                "link": link
            }
        except:
            pass


sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

header = ["name", "price", "link"]

with open('./Newegg/Newegg_Products.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for item in sorted_items:
        writer.writerow([item[0], f"${item[1]['price']}", item[1]['link']])

file.close()

Done = pyfiglet.figlet_format("Done")
print(Done)
