with open("corps.txt") as f:
  corps = f.read()

table = {}

for i in corps:
  if not i in table:
    table[i] = 0
  table[i] += 1

table_sort = sorted(list(table.items()), key=lambda x: x[1], reverse=True)

for i in table_sort:
  print(i)