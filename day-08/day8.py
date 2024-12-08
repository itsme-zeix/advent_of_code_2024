def process_input():
  with open("./day-08/input.txt", "r") as f:
    matrix = [list(line.strip()) for line in f.readlines()]

    antenna_mappings = {}
    for y in range(len(matrix)):
      for x in range(len(matrix[0])):
        antenna = matrix[y][x]
        if antenna == ".":
          continue
        if antenna in antenna_mappings:
          antenna_mappings[antenna].append((x, y))
        else:
          antenna_mappings[antenna] = [(x, y)]

    return matrix, antenna_mappings

def is_within_bounds(x, y):
  max_rows = len(matrix)
  max_cols = len(matrix[0])
  return x >= 0 and x < max_rows and y >= 0 and y < max_cols

def solve_part1():
  # For each antenna type, we check every other of the same antenna type to
  # determine mapping.
  antinodes = set()

  for _, antenna_coordinates in antenna_mappings.items():
    for antenna1 in antenna_coordinates:
      for antenna2 in antenna_coordinates:
        if antenna1 == antenna2:
          continue

        x1, y1 = antenna1
        x2, y2 = antenna2
        dx, dy = x2 - x1, y2 - y1
        antinode = (x2 + dx, y2 + dy)

        if is_within_bounds(antinode[0], antinode[1]):
          antinodes.add(antinode)

  return len(antinodes)

def solve_part2():
  antinodes = set()

  for _, antenna_coordinates in antenna_mappings.items():
    for antenna1 in antenna_coordinates:
      for antenna2 in antenna_coordinates:
        if antenna1 == antenna2:
          continue

        x1, y1 = antenna1
        x2, y2 = antenna2
        dx, dy = x2 - x1, y2 - y1
        
        multiplier = 0
        is_antinode_within_bounds = True
        while is_antinode_within_bounds:
          antinode = (x2 + dx * multiplier, y2 + dy * multiplier)

          is_antinode_within_bounds = is_within_bounds(antinode[0], antinode[1])

          if is_antinode_within_bounds:
            antinodes.add(antinode)

          multiplier += 1

  return len(antinodes)

if __name__ == "__main__":
  matrix, antenna_mappings = process_input()
  print(f"Part 1: {solve_part1()}")
  print(f"Part 2: {solve_part2()}")
