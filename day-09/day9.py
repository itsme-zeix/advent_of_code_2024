def process_input():
  with open ("./day-09/input.txt", "r") as f:
    input = f.read().strip()
    return input

def solve_part1():
  files = []
  for id in range(0, len(input)):
    character = id // 2 if id % 2 == 0 else "."
    repeats = int(input[id])
    files.extend([character] * repeats)

  total = 0
  i, j = 0, len(files) - 1
  while i < len(files):
    if files[i] != ".":
      i += 1
      continue
    # Avoided modifying the files array and instead updated the index j
    # to avoid re-building the list (at O(n) cost) in each iteration.
    while files[j] == ".":
      files[j] = 0
      j -= 1
    files[i] = files[j]
    files[j] = 0
    j -= 1
    i += 1

  total = sum(c * i for i, c in enumerate(files))
  return total

def solve_part2():
  files = []
  for id in range(0, len(input)):
    character = id // 2 if id % 2 == 0 else "."
    repeats = int(input[id])
    files.extend([character] * repeats)

  dots = [] # each dot = [start idx, end idx, count]
  nums = [] # each num = [start idx, end idx, count, char] 
  
  i = 0
  while i < len(files):
    starting_index = i
    starting_char = files[starting_index]
    while i + 1 < len(files) and files[i + 1] == starting_char:
      i += 1
    
    if starting_char == ".":
      dots.append([starting_index, i, i - starting_index + 1, starting_char])
    else:
      nums.append([starting_index, i, i - starting_index + 1, starting_char])

    i += 1 

  nums.reverse() # reverse nums so we can iterate through more easily.

  for num_grp in nums:
    for dot_grp in dots:
      if num_grp[2] > dot_grp[2]:
        pass
      elif num_grp[2] == dot_grp[2] and num_grp[0] > dot_grp[0]:
        num_grp[0] = dot_grp[0]
        num_grp[1] = dot_grp[1]
        dots.remove(dot_grp)
        break
      elif num_grp[2] < dot_grp[2] and num_grp[0] > dot_grp[0]:
        num_grp[0] = dot_grp[0]
        num_grp[1] = dot_grp[0] + num_grp[2] - 1
        dot_grp[0] += num_grp[2]
        dot_grp[2] = dot_grp[1] - dot_grp[0] + 1
        break
  # Spent forever on the above because i missed out the num_grp[0] > dot_grp[0] condition

  total = 0
  for num_grp in nums:
    for mul in range(num_grp[0], num_grp[1] + 1):
      total += int(num_grp[3]) * mul

  return total

if __name__ == "__main__":
  input = process_input()
  print(solve_part1())
  print(solve_part2())
