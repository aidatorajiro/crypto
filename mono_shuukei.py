#付きは確定

with open('corps.txt') as f:
    data = f.read()

out = {}

n = 4

for i in range(len(data) - n):
  k = data[i:i+n]
  if '\n' in k:
    continue
  if not k in out:
    out[k] = 0
  out[k] += 1

for i in sorted(list(out.items()), key=lambda x: x[1], reverse=True):
  s = i[0]
  #if i[0][1] == i[0][4] and i[0][2] == i[0][3] and i[0][0] != i[0][1] and i[0][0] != i[0][2]:   #datta
  #if s[1] == s[5] and s[0] == s[4] and len(set(s)) == 6:  #namonaki
  #if s[2] == ',': #wa, ga, etc.
  #if s[2] == s[3] and len(set(s)) == 4: #minna
  #if s[0] == s[2] and len(set(s)) == 4:
  # if s[2] == s[3] and len(set(s)) == 4:
  #if len(set(s)) == 5:
  #if len(set(s)) == 3 and s[1] == s[3]: #koto
    print(i)
