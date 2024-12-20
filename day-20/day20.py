from collections import deque

def process_input():
  with open("./day-20/input.txt", "r") as f:
    matrix = [list(line.strip()) for line in f.readlines()]
    start, end = (-1, -1), (-1, -1)
    for y in range(len(matrix)):
      for x in range(len(matrix[0])):
        if matrix[y][x] == "S": start = (x, y)
        if matrix[y][x] == "E": end = (x, y)
    return matrix, start, end

def bfs(mat, origin):
  q = deque([(origin[0], origin[1], 0)])
  distances = {origin: 0}
  dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

  while q:
    x, y, steps = q.popleft()

    for dx, dy in dirs:
      nx, ny = x + dx, y + dy
      if (0 <= nx < len(mat[0]) and 0 <= ny < len(mat)
          and (nx, ny) not in distances and mat[ny][nx] != "#"):
        distances[(nx, ny)] = steps + 1
        q.append((nx, ny, steps + 1))

  return distances

def solve():
  mat, start, end = process_input()

  # Part 1:
  from_start, to_end = bfs(mat, start), bfs(mat, end)
  steps_without_cheat = from_start[end]

  dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  part1 = 0
  for y in range(len(mat)):
    for x in range(len(mat[0])):
      if mat[y][x] != "#":
          continue

      valid_neighbors = []
      for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(mat[0]) and 0 <= ny < len(mat) and mat[ny][nx] != "#":
          valid_neighbors.append((nx, ny))

      for i, (nx1, ny1) in enumerate(valid_neighbors):
        for j in range(i + 1, len(valid_neighbors)):
          nx2, ny2 = valid_neighbors[j]

          steps_with_cheat = min(
            from_start[(nx1, ny1)] + to_end[(nx2, ny2)] + 2,
            from_start[(nx2, ny2)] + to_end[(nx1, ny1)] + 2
          )
          part1 += 1 if steps_without_cheat - steps_with_cheat >= 100 else 0

  # Part 2:
  tracks = [(x, y) for y in range(len(mat)) for x in range(len(mat[0])) if mat[y][x] != "#"]

  part2 = 0
  for i, (x1, y1) in enumerate(tracks):
    for j in range(i + 1, len(tracks)): 
      x2, y2 = tracks[j]

      manhattan_distance = abs(x1 - x2) + abs(y1 - y2)
      if manhattan_distance > 20:
        continue

      steps_with_cheat = min(
        from_start[(x1, y1)] + to_end[(x2, y2)] + manhattan_distance,
        from_start[(x2, y2)] + to_end[(x1, y1)] + manhattan_distance
      )
      part2 += 1 if steps_without_cheat - steps_with_cheat >= 100 else 0

  return part1, part2


if __name__ == "__main__":
  print(solve())
