import time

def process_input():
  with open("./day-11/input.txt", "r") as f:
    data = f.read().split()
    data = list(map(int, data))
    return data


def solve_part1(data, completed_blinks, blinks_required):
  if completed_blinks == blinks_required:
    return len(data)

  new_data = []
  for n in data:
    str_n = str(n)
    if n == 0:
      new_data.append(1)
    elif len(str_n) % 2 == 0:
      l = int(str_n[:len(str_n) // 2])
      r = int(str_n[len(str_n) // 2:])
      new_data.append(l)
      new_data.append(r)
    elif (len(str_n)) % 2 == 1:
      new_data.append(n * 2024)
  
  return solve_part1(new_data, completed_blinks + 1, blinks_required)

def solve_part2(data, blinks_required):
  # Optimization of part 1:
  # 1. Added memoization to map each number to its output upon 
  #    expansion to reduce redundant computation.
  # 2. Since order does not matter, a dictionary was used to keep track of the 
  #    number of times each number appears in the data. 
  #    Using the dict, we can expand the number once and multiply by the number of 
  #    times that the new number appears.
   
  counter = {} # Maps each number to the number of times it appears in data
  memoized = {} # Maps each number to its expansion

  # Build counter dict
  for n in data:
    counter[n] = counter[n] + 1 if n in counter else 1

  # Expand all numbers to get final counter dict
  for _ in range(blinks_required):
    counter = expand(counter, memoized)

  return sum(count for _, count in counter.items())

 
def expand(counter, memoized):
  new_counter = {}

  for n, count in counter.items():
    str_n = str(n)

    if n in memoized:
      for k in memoized[n]:
        new_counter[k] = new_counter.get(k, 0) +  count
      continue
    
    if n == 0:
      new_counter[1] = new_counter.get(1, 0) + count
      memoized[n] = [1]
    elif len(str_n) % 2 == 0:
      l = int(str_n[:len(str_n) // 2])
      r = int(str_n[len(str_n) // 2:])
      new_counter[l] = new_counter.get(l, 0) + count
      new_counter[r] = new_counter.get(r, 0) + count
      memoized[n] = [l, r]
    else:
      memoized[n] = [n * 2024]
      new_counter[n * 2024] = new_counter.get(n * 2024, 0) + count

  return new_counter


if __name__ == "__main__":
  data = process_input()
  print(f"Part 1 solution: {solve_part1(data, 0, 25)}")
  print(f"Part 1 solution: {solve_part2(data, 75)}")


