def process_input():
  with open("./day-04/input.txt", "r") as f:
    matrix = f.read().splitlines()
    rows = len(matrix)
    cols = len(matrix[0])
    return matrix, rows, cols

def check_part1(x, y, letters, index, dx, dy):
  if index == len(letters):
    return 1
  
  nx, ny = x + dx, y + dy
  if 0 <= ny < rows and 0 <= nx < cols:
    if matrix[ny][nx] == letters[index]:
      return check_part1(nx, ny, letters, index + 1, dx, dy)
  return 0

def solve_part1():
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
  res = 0

  for y in range(rows):
    for x in range(cols):
      if matrix[y][x] == 'X':
        for dx, dy in directions:
          res += check_part1(x, y, ['X', 'M', 'A', 'S'], 1, dx, dy)
  return res

def solve_part2():
  res = 0
  for r in range(rows):
    for c in range(cols):
      if matrix[r][c] == 'A':
        diagonal1 = False
        diagonal2 = False
        if 0 <= r + 1 < rows and 0 <= r - 1 < rows and 0 <= c + 1 < cols and 0 <= c - 1 < cols:
          diagonal1 = (matrix[r + 1][c + 1] == "M" and matrix[r - 1][c - 1] == "S") or \
            (matrix[r + 1][c + 1] == "S" and matrix[r - 1][c - 1] == "M")
          diagonal2 = (matrix[r + 1][c - 1] == "M" and matrix[r - 1][c + 1] == "S") or \
            (matrix[r + 1][c - 1] == "S" and matrix[r - 1][c + 1] == "M")
        if diagonal1 and diagonal2:
          res += 1
  return res

if __name__ == "__main__":
  matrix, rows, cols = process_input()
  print(solve_part1())
  print(solve_part2())
