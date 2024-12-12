def process_input():
  with open("./day-12/input.txt", "r") as f:
    return [list(line.strip()) for line in f]

def solve_part1():
  visited = set()
  total_price = 0

  for y in range(len(matrix)):
    for x in range(len(matrix[0])):
      if ((x,y)) not in visited:
        area, perimeter = bfs_part1(x, y, matrix[y][x], visited)
        total_price += area * perimeter

  return total_price

def bfs_part1(x, y, char, visited):
  queue = [(x, y)]
  visited.add((x,y))
  area = 0
  perimeter = 0
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

  while len(queue) != 0:
    cx, cy = queue.pop(0)
    area += 1

    for dx, dy in directions:
      nx, ny = cx + dx, cy + dy
      if not is_valid(nx, ny) or matrix[ny][nx] != char:
        perimeter += 1
      elif (nx, ny) not in visited:
        visited.add((nx, ny))
        queue.append((nx, ny))

  return area, perimeter

def solve_part2():
  plots = []
  visited = set()

  for y in range(len(matrix)):
    for x in range(len(matrix[0])):
      if ((x,y)) not in visited:
        area, sides = bfs_part2(x, y, matrix[y][x], visited)
        plots.append((area, list(sides)))

  total = 0
  for area, sides in plots:
    price = area * calc_no_of_sides(sides)
    total += price
  return total

def bfs_part2(x, y, char, visited):
  queue = [(x, y)]
  visited.add((x,y))
  area = 0
  sides = set()
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

  while len(queue) != 0:
    cx, cy = queue.pop(0)
    area += 1

    for dx, dy in directions:
      nx, ny = cx + dx, cy + dy
      if not is_valid(nx, ny) or matrix[ny][nx] != char:
        sides.add((cx, cy, dx, dy))
      elif (nx, ny) not in visited:
        visited.add((nx, ny))
        queue.append((nx, ny))

  return area, sides

def calc_no_of_sides(sides):
  counted = set()
  no_of_sides = 0

  sides.sort() # Need to sort due to the "adjacent checking" logic used below.

  for side in sides:
    cx, cy, dx, dy = side
    # Sides are adjacent (no_of_sides not incremented) if they have the 
    # same dx and their cy differs by 1 (or same dy and their cx differs by 1). 
    # Hence the need to sort the sides array above.
    if dx != 0 and (cx, cy+1, dx, dy) not in counted and (cx, cy-1, dx, dy) not in counted:
      no_of_sides += 1
    if dy != 0 and (cx+1, cy, dx, dy) not in counted and (cx-1, cy, dx, dy) not in counted:
      no_of_sides += 1
    counted.add((cx, cy, dx, dy))

  return no_of_sides

def is_valid(x, y):
  return x >= 0 and y >= 0 and y < len(matrix) and x < len(matrix[0])

if __name__ == "__main__":
  matrix = process_input()
  print(f"Part 1: {solve_part1()}")
  print(f"Part 2: {solve_part2()}")

