import csv
from pathlib import Path

menu_filepath = Path('../Resources/menu_data.csv')
sales_filepath = Path('../Resources/sales_data.csv')

menu = []
sales = []

with open(menu_filepath, 'r') as menufile:
  menureader = csv.reader(menufile, delimiter=",")
  header = next(menureader)

  for i in menureader:
    menu.append(i)
  
with open(sales_filepath, 'r') as salesfile:
  salesreader = csv.reader(salesfile, delimiter=',')
  header = next(salesreader)

  for i in salesreader:
    sales.append(i)

report = {}

for i in sales:
  quanity = i[3]
  sales_item = i[4]
  if sales_item not in report:
    report[sales_item] = { "01-count": 0, "02-revenue": 0, "03-cogs": 0, "04-profit": 0 }
  for i in menu:
    item = i[0]
    price = i[3]
    cost = i[4]
    if item == sales_item:
      report[sales_item]["01-count"] += int(quanity)
      report[sales_item]["02-revenue"] += int(quanity) * int(price)
      report[sales_item]["03-cogs"] += int(quanity) * int(cost)
      report[sales_item]["04-profit"] += (int(quanity) * int(price)) - (int(quanity) * int(cost))
    else:
      print(f"{sales_item} does not equal {item}! NO MATCH!")

with open ('output_file.txt', 'w') as file:
  for i in report:
    file.write(f"{i} {report[i]}")
    file.write("\n")