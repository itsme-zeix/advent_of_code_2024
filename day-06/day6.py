from enum import Enum
import time

def process_input():
  with open("./day-06/input.txt", "r") as f:
    matrix = f.readlines()
    matrix = [list(line.strip()) for line in matrix]
    no_of_rows = len(matrix)
    no_of_cols = len(matrix[0])

    # Get coordinates of guard and obstacles
    guard_coord = (0, 0)
    obstacle_set = set()
    for x in range(no_of_cols):
      for y in range(no_of_rows):
        if matrix[y][x] == "#":
          obstacle_set.add((x, y))
        if matrix[y][x] == "^":
          guard_coord = (x, y)
    
    return matrix, obstacle_set, guard_coord
  
def has_exited(guard_coord):
  no_of_rows = len(matrix)
  no_of_cols = len(matrix[0])
  x, y = guard_coord
  return x < 0 or x >= no_of_rows or y < 0 or y >= no_of_cols

def met_obstacle(guard_coord, current_direction, obstacle_set):
  x, y = guard_coord
  if current_direction == Direction.UP:
    y -= 1
  elif current_direction == Direction.DOWN:
    y += 1
  elif current_direction == Direction.LEFT:
    x -= 1
  elif current_direction == Direction.RIGHT:
    x += 1
  return (x, y) in obstacle_set

def solve_part1():
  x, y = initial_guard_coord
  direction = Direction.UP
  visited = set()

  while True:
    if has_exited((x, y)):
      return visited, len(visited)

    visited.add((x,y))
    
    if met_obstacle((x, y), direction, obstacle_set):
      next_enum_value = (direction.value % len(Direction)) + 1
      direction = Direction(next_enum_value)
      continue

    if direction == Direction.UP:
      y -= 1
    elif direction == Direction.DOWN:
      y += 1
    elif direction == Direction.LEFT:
      x -= 1
    elif direction == Direction.RIGHT:
      x += 1


def has_loop(obstacle_set):
  visited = set()
  direction = Direction.UP
  x, y = initial_guard_coord

  while True:
    if has_exited((x, y)):
      break

    if (x, y, direction) in visited:
      return True
    
    visited.add((x, y, direction))

    if met_obstacle((x, y), direction, obstacle_set):
      direction = Direction(direction.value % len(Direction) + 1)
      continue

    if direction == Direction.UP:
      y -= 1
    elif direction == Direction.DOWN:
      y += 1
    elif direction == Direction.LEFT:
      x -= 1
    elif direction == Direction.RIGHT:
      x += 1

  return False

def solve_part2():
  # Brute force solution is to try every possibility for the new obstacles and check if 
  # the guard is stuck in a loop (visited set has an entry with the same coordinates and direction).
  #
  # Time complexity: O(mn) * O(mn) = O(m^2 * n^2) where matrix is m x n.
  # O(mn) possiblities of new obstacle
  # O(mn) for each simulation
  #
  # We only need to check whatever has been visited before in part 1 as only those coordinates 
  # can be reached by the guard.
  total_loops = 0
  possible_obstacles = visited_in_part1

  for obstacle in possible_obstacles:
    obstacle_set.add(obstacle) # Temporarily add a new obstacle to our set
    total_loops += 1 if has_loop(obstacle_set) else 0
    obstacle_set.remove(obstacle)

  return total_loops

if __name__ == "__main__":
  Direction = Enum("Direction", [("UP", 1), ("RIGHT", 2), ("DOWN", 3), ("LEFT", 4)])
  matrix, obstacle_set, initial_guard_coord = process_input()

  part1_start_time = time.time()
  visited_in_part1, part1_solution = solve_part1()
  part1_duration = time.time() - part1_start_time
  print(f"Part 1: {part1_solution}")
  print(f"Part 1 took {part1_duration:.4f} seconds to complete.")

  part2_start_time = time.time()
  part2_solution = solve_part2()
  part2_duration = time.time() - part2_start_time
  print(f"Part 2: {part2_solution}")
  print(f"Part 2 took {part2_duration:.4f} seconds to complete.")
