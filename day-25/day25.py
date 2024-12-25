def process_input():
  chunks = []
  with open("./day-25/input.txt", "r") as f:
    chunks = [line.split() for line in f.read().split('\n\n')]

  keys, locks = [], []
  for chunk in chunks:
    heights = [sum(line[j] == "#" for line in chunk) for j in range(len(chunk[0]))]

    if chunk[0][0] == "#": # Lock
      locks.append(heights)
    else:
      keys.append(heights)

  lock_height = len(chunks[0])
  return locks, keys, lock_height


def solve_part1():
  locks, keys, lock_height = process_input()
  return sum(1 for lock in locks
               for key in keys 
               if all(l + k <= lock_height for l, k in zip(lock, key)))


if __name__ == "__main__":
  print(solve_part1())
