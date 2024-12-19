def process_input():
  with open("./day-19/input.txt", "r") as f:
    towels, patterns = f.read().split('\n\n')
    towels = towels.split(', ')
    patterns = patterns.split('\n')[:-1]
    return towels, patterns

def solve_part1():
  towels, patterns = process_input()

  def helper(pattern, towels):
    if len(pattern) == 0:
      return 1
    for t in towels:
      if len(t) <= len(pattern) and pattern[:len(t)] == t:
        res = helper(pattern[len(t):], towels)
        if res:
          return res
    return 0

  total = 0
  for p in patterns:
    total += helper(p, towels)
  return total

def solve_part2():
  towels, patterns = process_input()
  cache = {} # memoization to avoid repeated work

  def helper(pattern, towels):
    if pattern in cache:
      return cache[pattern]

    if len(pattern) == 0:
      return 1

    res = 0
    for t in towels:
      if len(t) <= len(pattern) and pattern[:len(t)] == t:
        res += helper(pattern[len(t):], towels)

    cache[pattern] = res
    return res

  total = 0
  for p in patterns:
    total += helper(p, towels)
  return total

if __name__ == "__main__":
  print(solve_part1())
  print(solve_part2())
