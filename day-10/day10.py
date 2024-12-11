def process_input():
  with open("./day-10/input.txt", "r") as f:
    return [list(map(int, line.strip())) for line in f]
  


def solve():
  # Funnily enough, I solved part2 before part1 by misintepreting the question.
  # Part 1 is just part 2 but only counting unique coordinates for all 9s found.

  # Find starting points
  zeros = []
  for y in range(len(matrix)):
    for x in range(len(matrix[0])):
      if matrix[y][x] == 0:
        zeros.append((x, y))

  part1, part2 = 0, 0
  for zero in zeros:
    x, y = zero
    unique_nines = set()
    part2 += dfs(x, y, 0, unique_nines)
    part1 += len(unique_nines)
  return part1, part2

def dfs(x, y, digit, unique_nines):
  if digit == 9:
    unique_nines.add((x,y))
    return 1
  
  total = 0
  if is_valid(x, y + 1) and matrix[y + 1][x] == digit + 1:
    total += dfs(x, y + 1, digit + 1, unique_nines)
  if is_valid(x, y - 1) and matrix[y - 1][x] == digit + 1:
    total += dfs(x, y - 1, digit + 1, unique_nines)
  if is_valid(x - 1, y) and matrix[y][x - 1] == digit + 1:
    total += dfs(x - 1, y, digit + 1, unique_nines)
  if is_valid(x + 1, y) and matrix[y][x + 1] == digit + 1:
    total += dfs(x + 1, y, digit + 1, unique_nines)

  return total

def is_valid(x, y):
  return 0 <= x < len(matrix[0]) and 0 <= y < len(matrix)

if __name__ == "__main__":
  matrix = process_input()
  part1, part2 = solve()
  print(f"Part 1: {part1}")
  print(f"Part 2: {part2}")
