from copy import deepcopy

def process_input():
  with open("./day-24/input.txt", "r") as f:
    raw_values, raw_gates = [line.strip().split("\n") for line in f.read().split("\n\n")]
    
    values = {}
    for v in raw_values:
      wire, val = v.split(': ')
      values[wire] = int(val)

    gates = {} # key: output, val: (var1, var2, op)
    for g in raw_gates:
      op1, op, op2, _, output = g.split()
      gates[output] = (op1, op2, op)

    return values, gates

def part1():
  values, gates = process_input()

  while gates:
    gates_copy = deepcopy(gates)
    for output, (op1, op2, op) in gates_copy.items():
      if op1 not in values or op2 not in values:
        continue
      values[output] = alu(values[op1], values[op2], op)
      gates.pop(output)

  z_wires = []
  for wire in values:
    if wire[0] != 'z':
      continue
    z_wires.append(wire)
    
  z_wires.sort(reverse=True)

  bin = ''
  for wire in z_wires:
    bin += str(values[wire])

  return int(bin, 2)


def part2():
  # Cases = no. of ways to choose 8 items in 222 items * no. of permutations of 8 items
  #       = 222C8 * 8!
  #       = 5e18 (Cannot bruteforce)
  #
  # This seems like a ripple carry adder, so we could check correctness
  # for that. Worked out logic by hand:
  # carry_n = OR(AND(xn, yn), AND(carry_(n-1), XOR(xn, yn))
  # zn = XOR(carry_(n-1), XOR(xn, yn))

  _, gates = process_input()
  gates_to_output = {value: key for key, value in gates.items()}
  z_msb = max([i for i in gates if i[0] == 'z'], key=lambda k: int(k[1:]))

  incorrect = set()
  for (op1, op2, op), out in gates_to_output.items():
    # All 'z' outputs (except the MSB) are made by XOR operations.
    if out[0] == 'z' and op != "XOR" and out != z_msb:
      incorrect.add(out)
    
    # XOR operations that do not output 'z' must have operands x and y.
    if out[0] != 'z' and op == "XOR" and op1[0] not in {'x', 'y'} and op2[0] not in {'x', 'y'}:
      incorrect.add(out)

    # XOR operations that output 'z' must have an operand outputted from OR and XOR respectively,
    # except for the case of AND(x00, y00).
    if out[0] == 'z' and op == 'XOR':
      if op1 == "x00" or op2 == "x00":
        continue

      if gates[op1][2] == "OR" and gates[op2][2] != "XOR":
        if gates[op2][0] in {"x00", "y00"}: # Edge case for AND(x00, y00)
          continue
        incorrect.add(op2)
      elif gates[op1][2] == "XOR" and gates[op2][2] != "OR":
        if gates[op2][0] in {"x00", "y00"}: # Edge case for AND(x00, y00)
          continue
        incorrect.add(op2)

    # OR operations must have both operands outputted from AND operations.
    if op == "OR":
      if gates[op1][2] != "AND":
        incorrect.add(op1)
      elif gates[op2][2] != "AND":
        incorrect.add(op2)

  return ','.join(sorted(list(incorrect)))

def alu(x, y, operator):
  if operator == "AND": return x and y
  elif operator == "OR": return x or y
  elif operator == "XOR": return x ^ y

if __name__ == "__main__":
  print(part1())
  print(part2())
