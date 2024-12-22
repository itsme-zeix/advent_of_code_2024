from functools import cache
from itertools import permutations
import time

def process_input():
  with open("./day-21/input.txt", "r") as f:
    return f.read().split()

def solve(max_depth):
  codes = process_input()

  res = 0
  for code in codes:
    complexity = 0
    for i in range(len(code)):
      steps = step('A' if i == 0 else code[i - 1], code[i], 0, max_depth)
      complexity += steps
    res += complexity * int(code[:-1])
  return res

@cache
def step(curr, target, depth, max_depth):
  # At each step, we find the required movement and compute all permutations 
  # of horizontal/vertical movements.
  # 
  # We continue to step through each permutation until we reach our max depth,
  # choose the one with the minimum length, which backtracks to be summed up.

  if curr == target:
    return 1 # To press A 
  
  # Dynamically choose keypad
  pad = numpad if depth == 0 else arrowkeys
  cx, cy = pad[curr]
  tx, ty = pad[target]
  dx, dy = tx - cx, ty - cy

  # Base case
  if depth == max_depth:
    return abs(dx) + abs(dy) + 1 # +1 to press A

  # Advent of Brute Force. Somehow couldn't get horizontal/vertical permutations
  # to work properly (although it should theoretically be better to repeat moves)
  # so I just got all permutations and brute forced it...
  # Turns out it's not slow at all because of caching.
  moves = ''
  moves += '^' * -dy if dy < 0 else 'v' * dy
  moves += '<' * -dx if dx < 0 else '>' * dx
  perms = set(permutations(moves))
  print(perms)
  
  # Said 'horizontal/vertical permutations only' implementation:
  #
  # def get_valid_permutations(cx, cy, tx, ty, horizontal, vertical, pad):
  #   permutations = set()
  #   if (cx, ty) in pad.values():
  #     permutations.add(vertical + horizontal)
  #   if (tx, cy) in pad.values():
  #     permutations.add(horizontal + vertical)
  #   return permutations
  #
  # horizontal = '<' * -dy if dy < 0 else '>' * dy
  # vertical = '^' * -dx if dx < 0 else 'v' * dx
  # perms = get_valid_permutations(cx, cy, tx, ty, horizontal, vertical, pad)

  candidates = []
  for p in perms:
    pos = (cx, cy)
    steps = 0
    valid = True

    for i, button in enumerate(p):
      next_pos = move_position(pos, button)
      if next_pos not in pad.values():
        valid = False
        break
      steps += step('A' if i == 0 else p[i - 1], button, depth + 1, max_depth)
      pos = next_pos

    if valid:
      steps += step(p[-1], 'A', depth + 1, max_depth)
      candidates.append(steps)

  return min(candidates) if candidates else float('inf')

def move_position(pos, direction):
  x, y = pos
  if direction == '^': return (x, y-1)
  if direction == 'v': return (x, y+1)
  if direction == '<': return (x-1, y)
  if direction == '>': return (x+1, y)
  return pos

if __name__ == "__main__":
  numpad = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
                 '0': (1, 3), 'A': (2, 3)
  }
  arrowkeys = {
                 '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
  }

  print(f"Part 1: {solve(2)}")
  # curr= time.time()
  # print(f"Part 2: {solve(25)}")
  # print(time.time() - curr)
