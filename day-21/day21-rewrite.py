from functools import cache
import time

def process_input():
  with open("./day-21/input.txt", "r") as f:
    return f.read().split()

def solve(max_depth):
  codes = process_input()

  res = 0
  for code in codes:
    complexity = 0
    # Solve each character individually (expands recursively), before
    # summing up total cost of characters to make up each code.
    for i in range(len(code)):
      steps = step('A' if i == 0 else code[i - 1], code[i], 0, max_depth)
      complexity += steps
    # Add complexity (cost of pressing code) * code to the total.
    res += complexity * int(code[:-1]) 
  return res

@cache
def step(curr, target, depth, max_depth):
  # At each step, we find the required movement and compute all permutations 
  # of horizontal/vertical movements.
  # 
  # We continue to step through each permutation until we reach our max depth,
  # return the candidate with minimum length, which is then summed up as we close the recursion.

  # Dynamically choose keypad
  pad = numpad if depth == 0 else arrowkeys

  # Update coordinates and direction/amount to move
  cx, cy = pad[curr]
  tx, ty = pad[target]
  dx, dy = tx - cx, ty - cy

  # Base cases
  if curr == target:
    return 1 # To press A 

  if depth == max_depth:
    return abs(dx) + abs(dy) + 1 # +1 to press A
  
  # Generate valid permutations of movements:
  # Only add horizontal/vertical to permutations as >>>^ is strictly better than >^>>,
  # as >>>^ creates multiple repeated 'A' instructions that are cheaper than A + directions + A
  # since no movement is required for multiple 'A' instructions (robot just presses A again!).
  horizontal = '>' * dx if dx > 0 else '<' * -dx
  vertical = 'v' * dy if dy > 0 else '^' * -dy
  permutations = generate_valid_permutations(cx, cy, tx, ty, horizontal, vertical, pad)

  # Perform stepping on permutations and its buttons recursively and get min. cost/steps at
  # every level whcih sums up to get the overall best cost/steps.
  candidates = []
  for p in permutations:
    steps = 0
    for i, button in enumerate(p):
      steps += step('A' if i == 0 else p[i - 1], button, depth + 1, max_depth)
    candidates.append(steps)

  return min(candidates)

def generate_valid_permutations(cx, cy, tx, ty, horizontal, vertical, pad):
  permutations = set()
  # Each permutation could possibly enter an 'empty' space on the keypad as its moving from
  # the original key position to the target key position. 
  # These are invalid permutations which we will not add to the set of permutations.
  if (cx, ty) in pad.values():
    permutations.add(vertical + horizontal + 'A')
  if (tx, cy) in pad.values():
    permutations.add(horizontal + vertical + 'A')
  return permutations

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
  curr= time.time()
  print(f"Part 2: {solve(25)}")
  print(f"Part 2 took: {(time.time() - curr):.5f}s")
  # Part 2 takes only ~0.0008s!
