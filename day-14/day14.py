def process_input():
  data = []
  with open("./day-14/input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
      p, v = line.split()
      px, py = p[2:].split(",")
      vx, vy = v[2:].split(",")
      data.append((int(px), int(py), int(vx), int(vy)))
  return data

def solve_part1(width, height):
  seconds = 100

  updated_robot_coords = []
  for robot in data:
    (px, py, vx, vy) = robot
    nx = (px + seconds * vx) % (width)
    ny = (py + seconds * vy) % (height)
    updated_robot_coords.append((nx, ny))

  top_left = 0
  top_right = 0
  bot_left = 0
  bot_right = 0
  middle_coordinates = (width // 2, height // 2) # length and width always odd

  for robot_x, robot_y in updated_robot_coords:
    if robot_x == middle_coordinates[0] or robot_y == middle_coordinates[1]:
      continue
    if robot_x < middle_coordinates[0] and robot_y < middle_coordinates[1]:
      # Top Left
      top_left += 1
    elif robot_x < middle_coordinates[0] and robot_y > middle_coordinates[1]:
      # Bottom Left
      bot_left += 1
    elif robot_x > middle_coordinates[0] and robot_y < middle_coordinates[1]:
      # Top Right
      top_right += 1
    else:
      # Bottom Right
      bot_right += 1
  
  return top_left * bot_left * top_right * bot_right

def solve_part2(width, height):
  # Guessing that the xmas tree happens when a bunch of
  # robots line up along a row which makes up a certain percentage
  # of the total width.
  percent_of_width = 0.1
  for seconds in range(0, 100000):
    updated_robot_coords = set()
    for robot in data:
      (px, py, vx, vy) = robot
      nx = (px + seconds * vx) % (width)
      ny = (py + seconds * vy) % (height)
      updated_robot_coords.add((nx, ny))

    max_consecutive = 1
    current_consecutive = 1
    for y in range(width):
      for x in range(height):
        if (x, y) in updated_robot_coords:
          current_consecutive += 1
          max_consecutive = max(max_consecutive, current_consecutive)
        else:
          current_consecutive = 1
      current_consecutive = 1
    
    if max_consecutive >= percent_of_width * width:
      return seconds

  return -1 # No result found, adjust percent_of_width
  

if __name__ == "__main__":
  data = process_input()
  print(solve_part1(101, 103))
  print(solve_part2(101,103))
