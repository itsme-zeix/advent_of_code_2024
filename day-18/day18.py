from collections import deque
import time

def process_input():
  with open("day-18/input.txt", "r") as f:
    input = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]
    return input

def solve_part1():
  input = process_input()
  matrix = [['.' for _ in range(71)] for _ in range(71)]

  # Only first kilobyte required
  walls = set()
  for i in range(1024):
    walls.add(input[i])
  return bfs(matrix, walls)

def solve_part2():
  input = process_input()
  matrix = [['.' for _ in range(71)] for _ in range(71)]

  # Currently brute forced and runs in about ~3s with pypy3, can be optimized by
  # continuing bfs with an added wall whenever there is a solution to the bfs.
  walls = set()
  for i in range(len(input)):
    if i < 1024: pass
    walls.add(input[i])

    # No solution
    if not bfs(matrix, walls):
      return input[i]
  return None

def bfs(matrix, walls):
  q = deque()
  visited = set()
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  q.append((0, 0, 0))

  while q:
    x, y, steps = q.popleft()
    if (x, y) == (70, 70):
      return steps
    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if (nx, ny) not in walls and 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
        if (nx, ny) not in visited:
          visited.add((nx, ny))
          q.append((nx, ny, steps + 1))
  return None

if __name__ == "__main__":
  print(f"Part 1: {solve_part1()}")
  start = time.time()
  print(f"Part 2: {solve_part2()}")
  elapsed = time.time()
  print(elapsed - start)
