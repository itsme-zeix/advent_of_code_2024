def process_input():
  with open("day-17/input.txt", "r") as f:
    A, B, C = 0, 0, 0
    program = []

    for line in f:
      line = line.strip()
      if line.startswith("Register"):
        register, value = line.split(": ")
        if register.endswith("A"): A = int(value)
        elif register.endswith("B"): B = int(value)
        elif register.endswith("C"): C = int(value)
      elif line.startswith("Program"):
         program = list(map(int, line.split(": ")[1].split(",")))

    return A, B, C, program

def run(A, B, C, program):
  def get_operand_value(operand):
    if operand in {0, 1, 2, 3}: return operand
    elif operand == 4: return A
    elif operand == 5: return B
    elif operand == 6: return C
    else: return -1

  output = []
  i = 0
  while i < len(program):
    opcode = program[i]
    operand = program[i + 1]

    if opcode == 0: A = A // (2 ** get_operand_value(operand))
    elif opcode == 1: B ^= operand # XOR
    elif opcode == 2: B = get_operand_value(operand) % 8
    elif opcode == 3 and A != 0:
      i = operand
      continue
    elif opcode == 4: B ^= C
    elif opcode == 5: output.append(get_operand_value(operand) % 8)
    elif opcode == 6: B = A // 2 ** get_operand_value(operand)
    elif opcode == 7: C = A // 2 ** get_operand_value(operand)

    i += 2

  return output

def solve_part1():
  A, B, C, program = process_input()
  ansList = run(A, B, C, program)
  return ','.join(str(num) for num in ansList)

def solve_part2():
  A, B, C, program = process_input()
  A = 1

  # Find smallest A such that output and program length are the same.
  program_length = len(program)
  best = 0
  while True:
    output = run(A, B, C, program)
    if len(output) > best and len(output) <= program_length:
      best = len(output)
      print(A, oct(A), best, program_length) # Progress tracker for viewing
      if len(output) == program_length:
        break
    A *= 2

  # From the output of the above code, there's a pattern where an additional digit is added 
  # to the output whenever A = A * 8.
  # This means that the octal is being "left shifted" by 1.
  # Therefore, correct_A = n ** 8 + some constant between 1 and 8
  #
  # To solve, we can add a constant from 0 to 8 to A and see if the output matches the program's 
  # last few digits (since the last digits happen after the big num is divided down).
  # If it matches, we can do an octal shift (multiply by 8) to attempt to find the larger A
  # that produces the next matching digit on the left. 
  # Repeat this recursively until output is entirely the same as program.
  def helper(A, program, cursor):
    for k in range(8):
      if run(A * 8 + k, 0, 0, program) == program[cursor:]:
        new_A = A * 8 + k
        if cursor == 0:
          return new_A
        res = helper(new_A, program, cursor - 1)
        if res is not None:
          return res
    return None

  return helper(0, program, len(program) - 1)

if __name__ == "__main__":
  print(f"Part 1: {solve_part1()}")
  print(f"Part 2: {solve_part2()}")

