def process_input():
  with open("./day-05/input.txt", "r") as f:
    lines = f.readlines()
    rules = set()
    updates = []
    isUpdate = False
    for line in lines:
      if line == "\n":
        isUpdate = True
      elif isUpdate:
        parsed_update = line.strip().split(",")
        updates.append(parsed_update)
      else:
        rules.add(line.strip())
    return rules, updates

def is_allowed(update):
  return not any(
    f"{update[j]}|{update[i]}" in rules
    for i in range(len(update))
    for j in range(i + 1, len(update))
  )

def solve_part1():
  # O(n^2) where n is the length of input but n is small here. /shrug
  total = 0
  for update in updates:
    if is_allowed(update):
      middle_number = int(update[len(update) // 2])
      total += middle_number
  return total

def solve_part2():
  # Thought about doing topo sort but there are cycles and I didn't really want to handle that separately.
  total = 0
  for update in updates: # O(n^3), kinda nasty but works
    fixed = False
    
    while not fixed:
      fixed = True
      for i in range(len(update)):
        for j in range(i + 1, len(update)):
          if f"{update[j]}|{update[i]}" in rules:
            update[j], update[i] = update[i], update[j]
            fixed = False # Another pass is needed as a swap was done

    middle_number = int(update[len(update) // 2])
    total += middle_number

  return total - part1_solution

if __name__ == "__main__":
  rules, updates = process_input()
  part1_solution = solve_part1()
  print(part1_solution)
  print(solve_part2())
