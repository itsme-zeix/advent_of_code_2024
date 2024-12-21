import time
from functools import lru_cache

def process_input():
  with open("./day-21/input.txt", "r") as f:
    codes = [i.strip() for i in f.readlines()]
    return codes

def solve(max_depth):
  codes = process_input()

  coords = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
                 '0': (1, 3), 'A': (2, 3)
  }

  res = 0
  for code in codes:
    commands = {""}
    curr = (2, 3) # Start at A
    for ch in code:
      target = coords[ch]
      commands = {
        existing + new 
        for existing in commands 
        for new in move(curr, target, (0, 3))
      } # Using a set to avoid duplicates
      curr = target

    # Propagate commands to higher level robot `max_depth` times
    now = time.time()
    for depth in range(max_depth):
      # Store a count of each character. Convert char to instruction once, then
      # multiply the length of instruction and the count.
      print(f"depth: {depth}, {time.time() - now}")
      temp = set()
      for c in commands:
        next = compute_for_next_robot(c)
        temp = temp.union(next)

      commands = temp

    res += min(map(len, commands)) * int(code[:-1])

  return res

@lru_cache
def compute_for_next_robot(commands):
  coords = {
                 '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
  }
  
  curr = (2, 0)
  converted_commands = [""]
  for ch in commands:
    target = coords[ch]
    converted_commands = {
      existing + new 
      for existing in move(curr, target, (0, 0)) 
      for new in converted_commands
    } # Using a set to avoid duplicates
    curr = target

  return converted_commands

@lru_cache
def move(curr, target, invalid_coord):
  x_commands = ""
  y_commands = ""
  dx = target[0] - curr[0]
  dy = target[1] - curr[1]

  if dx > 0:
    x_commands = ">" * dx
  elif dx < 0:
    x_commands = "<" * -dx

  if dy > 0:
    y_commands = "v" * dy
  elif dy < 0:
    y_commands = "^" * -dy

  # Doing horizontally only then vertically only (vice versa) is
  # more efficient than a mix of them. (i.e. >>>^^ is better than >^^>>).
  # Decide whether to do vertical or horizontal commands first based on whether
  # it leads to an invalid coordinate. 

  if invalid_coord == (curr[0], curr[1] + dy):
    # Do x first
    return [x_commands + y_commands + "A"]
  elif invalid_coord == (curr[0] + dx, curr[1]):
    # Do y first
    return [y_commands + x_commands + "A"]
  elif dx < 0:
    return [x_commands + y_commands + "A"]
  else:
    return [y_commands + x_commands + "A"]

if __name__ == "__main__":
  curr = time.time()
  print(f"Part 1: {solve(2)}")
  print(f"Part 2: {solve(25)}")
  elapsed = time.time()
  print(elapsed-curr)
