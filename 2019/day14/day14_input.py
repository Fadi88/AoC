from collections import defaultdict
import itertools
import math
import os.path
import re
import sys



def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  reactions = {}
  for line in input.split('\n'):
    match = re.search(r'^((?:\d+ [A-Z]+, )*\d+ [A-Z]+) => (\d+) ([A-Z]+)$', line)
    output_amount = int(match.group(2))
    output = match.group(3)
    inputs = []
    for input in match.group(1).split(', '):
      input_amount, input = input.split(' ')
      inputs.append((int(input_amount), input))
    reactions[output] = (output_amount, inputs)
  return reactions


def calc_ore(reactions, target, target_amount, surplus=None):
  if surplus is None:
    surplus = defaultdict(int)
  if target == 'ORE':
    return target_amount
  elif target_amount <= surplus[target]:
    surplus[target] -= target_amount
    return 0
  target_amount -= surplus[target]
  surplus[target] = 0
  ore = 0
  output_amount, inputs = reactions[target]
  copies = math.ceil(target_amount / output_amount)
  for input_amount, input in inputs:
    input_amount *= copies
    ore += calc_ore(reactions, input, input_amount, surplus)
  surplus[target] += output_amount * copies - target_amount
  return ore


def part1(reactions):
  return calc_ore(reactions, 'FUEL', 1)


def part2(reactions):
  ore = 1000000000000
  target_amount = ore // part1(reactions)
  fuel = 0
  surplus = defaultdict(int)
  while ore and target_amount:
    new_surplus = defaultdict(int, surplus)
    ore_used = calc_ore(reactions, 'FUEL', target_amount, new_surplus)
    if ore_used > ore:
      target_amount //= 2
    else:
      fuel += target_amount
      ore -= ore_used
      surplus = new_surplus
  return fuel


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))