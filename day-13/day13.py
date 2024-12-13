import re
import numpy as np

def process_input():
  machines = []
  with open("./day-13/input.txt", "r") as f:
    input = f.read()
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    matches = re.findall(pattern, input)
    for match in matches:
      button_a = (int(match[0]), int(match[1]))
      button_b = (int(match[2]), int(match[3]))
      prize = (int(match[4]), int(match[5]))
      machines.append({"a": button_a, "b": button_b, "prize": prize})
  return machines

def solve_part1():
  total = 0
  for machine in machines:
    total += solve_machine_part1(machine)
  return total

def solve_machine_part1(machine):
  ax, ay = machine["a"]
  bx, by = machine["b"]
  px, py = machine["prize"]

  solutions = []

  for i in range(0, 101):
    for j in range(0, 101):
      if ax * i + bx * j == px and ay * i + by * j == py:
        cost = 3 * int(i) + int(j)
        solutions.append(cost)

  if len(solutions) == 0:
    return 0
  return min(solutions)

def solve_part2():
  # Only the 2nd and 4th machines are used
  relevant_machines = machines
  # Fix value
  for machine in relevant_machines:
    px, py = machine["prize"]
    machine["prize"] = (10000000000000 + px, 10000000000000 + py)

  # Instinctual reaction is binary search but I think there's a better solution that that
  # Pretty sure we can solve simultaneous equation for this
  total = 0
  for machine in relevant_machines:
    total += solve_machine_part2(machine)
  return total

def solve_machine_part2(machine):
  ax, ay = machine["a"]
  bx, by = machine["b"]
  px, py = machine["prize"]

  # eqn1: i*ax + j*bx = px
  # eqn2: i*ay + j*by = py
  #
  # Rearranging eqn1:
  # eqn3: j = (px - i*ax)/bx
  #
  # Substitute eqn3 into eqn2:
  # i*ay + by*(px - i*ax)/bx = py
  # i*ay*bx + by*px - i*ax*by = bx*py
  # eqn4: i = (bx*py - by*px) / (ay*bx - ax*by)
  #
  # Solve eqn4, then use it to solve eqn3:
  i = (bx * py - by * px) / (ay * bx - ax * by) if (ay * bx - ax * bx) != 0 else 0
  j = (px - i * ax) / bx if bx != 0 else 0
  if i >= 0 and j >= 0 and i.is_integer() and j.is_integer():
    return 3 * int(i) + int(j)
  return 0

if __name__ == "__main__":
  machines = process_input()
  print(solve_part1())
  print(solve_part2())

