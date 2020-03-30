#付きは確定

arr = [
    ('e', 'a'),
    ('0', 'i'),
    ('!', 'o'),
    ('9', 'u'),
    ('f', 'n'),
    ('6', 'e'),
    ('1', 't'),
    ('>', 'k'),
    ('a', 's'),
    ('s', 'r'),
    ('y', 'y'),
    ('/', 'h'),
    ('w', 'm'),
    ('m', 'w'),
    (';', 'd'),
    (',', 'g'),
    ('p', 'z'),
    ('&', 'b'),
    ('?', 'p'),
    ('.', 'f'),
    ('h', 'v'),
    ('q', ''),
    ('z', ''),
    ('[', ''),
    (']', ''),
    ('=', ''),
    ('*', ''),
    ('d', ''),
    ('(', ''),
    (')', ''),
    ('-', ''),
    ('u', ''),
    ('j', ''),
    ('t', ''),
]

trans = {}

for (i, j) in arr:
    if j != '':
        trans[i] = j

with open('corps.txt') as f:
    data = f.read()

out = ""

for i in data:
    if i == '\n':
        out += i
    else:
        if i in trans:
            out += trans[i]
        else:
            out += " "

print(out)


