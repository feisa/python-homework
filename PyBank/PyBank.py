from pathlib import Path
import csv
import sys

csvpath = Path('budget_data.csv')
line_num = 1
total_months = [] 
net_total = []
average_change = []

with open(csvpath, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader)
    # Print the header
    line_num += 1

    for i in csvreader:
      total_months.append(i[0])
      net_total.append(int(i[1]))

    for i in range(len(total_months)-1):
      average_change.append(int(net_total[i+1])-int(net_total[i]))
      print(average_change)
      print(net_total[i+1])
      print(net_total[i])

max_value = max(average_change)
min_value = min(average_change)
max_index = average_change.index(max_value)
min_index = average_change.index(min_value)
min_month = total_months[min_index + 1]
max_month = total_months[max_index + 1]

print(f"Financial Analysis")
print(f"----------------------------")
print(f"Total Months: {len(total_months)}")
print(f"Total: {sum(net_total)}")
print(f"Average Change: {round(sum(average_change)/len(total_months),2)}")
print(f"Greatest Increase in Profits: {max_month} ({max_value})")
print(f"Greatest Decrease in Profits: {min_month} ({min_value})")

with open('output_file.txt', 'w') as file:
  file.write(f"Financial Analysis")
  file.write("\n")
  file.write(f"----------------------------")
  file.write("\n")
  file.write(f"Total Months: {len(total_months)}")
  file.write("\n")
  file.write(f"Total: {sum(net_total)}")
  file.write("\n")
  file.write(f"Average Change: {round(sum(average_change)/len(total_months),2)}")
  file.write("\n")
  file.write(f"Greatest Increase in Profits: {max_month} ({max_value})")
  file.write("\n")
  file.write(f"Greatest Decrease in Profits: {min_month} ({min_value})")