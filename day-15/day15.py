from collections import deque

def process_input():
  with open("./day-15/input.txt", "r") as f:
    matrix = [list(line.strip()) for line in f.readlines()]

    boundary = set()
    boxes = set()
    robot = (0, 0)
    movements = deque()
    map = []

    for y in range(len(matrix)):
      if len(matrix[y]) and matrix[y][0] == "#":
        map.append(matrix[y])

      for x in range(len(matrix[y])):
        item = matrix[y][x]
        directions = {"<": (-1, 0), "^": (0, -1), "v": (0, 1), ">": (1, 0)}

        if item == "#":
          boundary.add((x, y))
        elif item == "O":
          boxes.add((x, y))
        elif item == "@":
          robot = (x, y)
        elif item in directions:
          movements.append(directions[item])

    fixed_matrix = [row for row in matrix if row and row[0] == '#']

    return fixed_matrix, boundary, boxes, robot, movements

def solve_part1():
  matrix, boundary, boxes, robot, movements = process_input()

  for dx, dy in movements:
    nx = robot[0] + dx
    ny = robot[1] + dy
    if (nx, ny) in boundary:
      continue

    # Attempt to move robot and boxes
    if (nx, ny) in boxes:
      if move_box(boundary, boxes, nx, ny, dx, dy):
        # Robot and boxes moved successfully
        robot = (nx, ny)
        continue
    else:
      robot = (nx, ny)

  print(generate_map_part1(matrix, boundary, boxes, robot)) # For verification

  # Calculate sum of boxes
  total = 0
  for (x, y) in boxes:
    total += y * 100 + x
  return total

def move_box(boundary, boxes, nx, ny, dx, dy):
  if (nx + dx, ny + dy) in boundary:
    return False # Cannot move any boxes

  if (nx + dx, ny + dy) in boxes:
    result = move_box(boundary, boxes, nx + dx, ny + dy, dx, dy)
    if result == False:  # Cannot move any boxes (Propagated from base case)
      return False
  
  boxes.remove((nx, ny))
  boxes.add((nx + dx, ny + dy))
  return True

def generate_map_part1(matrix, boundary, boxes, robot):
  output = ""
  for y in range(len(matrix)):
    for x in range(len(matrix[0])):
      if (x, y) in boundary:
        output += "#"
      elif (x, y) in boxes:
        output += "O"
      elif (x, y) == robot:
        output += "@"
      else:
        output += "."
    output += "\n"
  return output[:-1]

def solve_part2():
  # Rewrote solution multiple times. Can get difficult and messy due to 
  # having to shift vertical obstacles and propagate the changes beyond
  # just the x-coordinate of the robot.
  #
  # eg. Upward movement of robot(@)
  # # # # # # #         # # # # # # 
  # #         #         # [][][]  #
  # # [][][]  #         #  [][]   #
  # #  [][]   # ------> #   []    #
  # #   []    #         #   @     #
  # #   @     #         #         #
  # # # # # # #         # # # # # #

  matrix, _, _, robot, movements = process_input()

  # Build part 2 matrix (the warehouse)
  new_matrix = []
  for i in range(len(matrix)):
    new_matrix.append([])
    for c in matrix[i]:
      if c == '@':
        new_matrix[i].extend(['@', '.'])
      elif c == '#':
        new_matrix[i].extend(['#', '#'])
      elif c == 'O':
        new_matrix[i].extend(['[', ']'])
      elif c == '.':
        new_matrix[i].extend(['.', '.'])
      else:
        raise Exception(f"Error occured: Unexpected character {c} in matrix")

  robot = (robot[0] * 2, robot[1]) # Update robot coordinates

  for dx, dy in movements:
    boxes_to_move =  build_boxes_to_move(new_matrix, robot[0], robot[1], dx, dy)

    # Ensure that all boxes can be moved to new position
    if all(new_matrix[y + dy][x + dx] == '.' for (x, y, _) in boxes_to_move):
      # Move boxes
      for (x, y, half_box) in boxes_to_move:
        new_matrix[y + dy][x + dx] = half_box
      # Move robot
      robot = (robot[0] + dx, robot[1] + dy)
    else:
      # Revert the replaced boxes
      for (x, y, half_box) in boxes_to_move:
        new_matrix[y][x] = half_box


  printable = "\n".join("".join(line) for line in new_matrix)
  print(printable)
  # Get final answer
  total = 0
  for y in range(len(new_matrix)):
    for x in range(len(new_matrix[0])):
      if new_matrix[y][x] == '[':
        total += 100 * y + x
  return total
  

def build_boxes_to_move(matrix, x, y, dx, dy):
  if not is_valid(matrix, x, y):
    return []

  if matrix[y][x] == '#' or matrix[y][x] == '.':
    return []

  half_box = matrix[y][x]
  boxes_to_move = [(x, y, half_box)]  # Starting box position
  matrix[y][x] = '.' # Rewrite existing box to empty space

  # Recursively find all box positions
  if is_valid(matrix, x + dx, y + dy):
    boxes_to_move.extend(build_boxes_to_move(matrix, x + dx, y + dy, dx, dy))

  # Add the other half of the box
  if half_box == "[":
    boxes_to_move.extend(build_boxes_to_move(matrix, x + 1, y, dx, dy))
  if half_box == "]":
    boxes_to_move.extend(build_boxes_to_move(matrix, x - 1, y, dx, dy))

  return boxes_to_move

def is_valid(matrix, nx, ny):
  return 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix)

if __name__ == "__main__":
  print(f"Part 1 solution: {solve_part1()}\n")
  print(f"Part 2 solution: {solve_part2()}")


