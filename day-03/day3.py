import re

def process_input():
  with open("./day-03/input.txt", "r") as f:
    return f.read().replace("\n", " ")

def multiply(x, y):
  return int(x) * int(y)

def solve_part1(input):
  regex_exp_mul = r'mul\((\d+),(\d+)\)'
  matches = re.findall(regex_exp_mul, input)

  total = 0
  for x, y in matches:
    total += multiply(x,y)
  return total

def solve_part2(input):
  # Add do() to the start of the input and don't() to the end of the input.
  # This will allow us to capture all groups between do() and don't().
  # We will need to do non-greedy matching otherwise we won't be able to capture
  # groups within the most outer do() and don't().

  # Interestingly was stuck here for awhile due to the presence of new lines `\n`,
  # which needed to be replaced as it affected pattern matching.

  updated_input = "do()" + input + "don't()"
  regex_exp_activated_input = r'do\(\)(.*?)don\'t\(\)'
  activated_inputs = re.findall(regex_exp_activated_input, updated_input)

  total = 0
  for activated_input in activated_inputs:
    total += solve_part1(activated_input)
  return total

if __name__ == "__main__":
  input_text = process_input()
  print(solve_part1(input_text))
  print(solve_part2(input_text))