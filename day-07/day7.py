def process_input():
  with open("./day-07/input.txt", "r") as f:
    lines = f.readlines()

    results = []
    components = []
    for line in lines:
      result = line.split()[0][:-1]
      results.append(result)
      curr_components = line.split()[1:]
      components.append(curr_components)

    return results, components

def part1_helper(target_total, curr_total, components, index):
  if curr_total == target_total and index == len(components):
    return True
  if index >= len(components) or curr_total >= target_total:
    return False

  curr_component = int(components[index])
  plus = part1_helper(target_total, curr_total + curr_component, components, index + 1)
  multiply = part1_helper(target_total, curr_total * curr_component, components, index + 1) 
  return plus or multiply

def solve_part1():
  total = 0
  for i in range(len(results)):
    result = int(results[i])
    curr_components = components[i]
    if part1_helper(result, int(curr_components[0]), curr_components, 1):
      # intially did part1_helper(result, 0, curr_components, 1), but this allowed the first 
      # number to be muliplied by 0 which produces an incorrect result.
      total += result
  return total

def part2_helper(target_total, curr_total, components, index):
  if curr_total == target_total and index == len(components):
    return True
  if index >= len(components) or curr_total > target_total:
    return False

  curr_component_string = components[index]
  plus = part2_helper(target_total, curr_total + int(curr_component_string), components, index + 1)
  multiply = part2_helper(target_total, curr_total * int(curr_component_string), components, index + 1)
  # String abuse xd
  concat = part2_helper(target_total, int(str(curr_total) + curr_component_string), components, index + 1) 
  return plus or multiply or concat

def solve_part2():
  total = 0
  for i in range(len(results)):
    result = int(results[i])
    curr_components = components[i]
    if part2_helper(result, int(curr_components[0]), curr_components, 1):
      total += result
  return total

if __name__ == "__main__":
  results, components = process_input()
  print(solve_part1())
  print(solve_part2())

