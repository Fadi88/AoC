import re

inp = open('input.txt').read().strip()

part2 = False

def day9b(d):
    bracket = re.search(r'\((\d+)x(\d+)\)', d)
    if not bracket:
        return len(d)
    pos = bracket.start(0)
    sz = int(bracket.group(1))
    rpt = int(bracket.group(2))
    i = pos + len(bracket.group())
    return len(d[:pos]) + day9b(d[i:i+sz]) * rpt + day9b(d[i+sz:])

print(day9b(inp))


