from collections import defaultdict
from heapq import heappush, heappop

def process_input():
  with open("./day-16/input.txt", "r") as f:
    matrix = [list(line.strip()) for line in f.readlines()]
    start = None
    end = None
    for y in range(len(matrix)):
      for x in range(len(matrix[0])):
        item = matrix[y][x]
        if item == "S":
          start = (x, y)
        if item == "E":
          end = (x, y)
    return matrix, start, end

def solve():
  matrix, start, end = process_input()

  # Djikstra's algorithm
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  reverse_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  best_cost = float("inf")
  queue = [(0, start, 0, [start])] # stores (cost, coordinates, dir+index, path)
  costs = defaultdict(lambda: float("inf"))
  paths = set()

  while queue:
    cost, coord, dir_index, path = heappop(queue)

    if cost > costs[(coord, dir_index)]:
      continue
    costs[(coord, dir_index)] = cost

    if coord == end and cost <= best_cost:
      pathSet = set(path)
      paths = paths | pathSet
      best_cost = cost # This is changeed once and never again due to the use of Djikstra's.
      # Djikstra's ensures the best cost if found as the first solution.

    for i, dir in enumerate(directions):
      # Check if we are going in the "reverse" direction AKA where we came from.
      if dir == reverse_directions[dir_index]:
        continue

      new_coord = (coord[0] + dir[0], coord[1] + dir[1])
      if is_valid(matrix, new_coord):
        if i == dir_index:
          heappush(queue, (cost + 1, new_coord, i, path + [new_coord]))
        else:
          heappush(queue, (cost + 1001, new_coord, i, path + [new_coord]))
  
  return best_cost, len(paths)

def is_valid(matrix, coordinate):
  x, y = coordinate
  return 0 <= x < len(matrix[0]) and 0 <= y < len(matrix) and matrix[y][x] != "#"

if __name__ == "__main__":
  part1_sol, part2_sol = solve()
  print(f"Part 1: {part1_sol}")
  print(f"Part 2: {part2_sol}")

