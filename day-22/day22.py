from collections import deque

def process_input():
  with open("./day-22/input.txt", "r") as f:
    return list(map(int, f.read().split()))

def solve_part1(secrets):
  updated_secrets = []
  for secret in secrets:
    for _ in range(2000):
      secret = transform(secret)
    updated_secrets.append(secret)
  return sum(updated_secrets)

def solve_part2(secrets):
  sequences = {} # key: sequence of the 4 changes as a tuple, value: sum of prices collected

  for secret in secrets:
    sequences_changed_for_this_secret = set() # Monkey buys the bananas the first time it sees a sequence.
    recent_changes = deque(maxlen=4)
    prev_price = secret % 10

    for _ in range(2000):
      secret = transform(secret)
      price = secret % 10

      change = price - prev_price
      prev_price = price

      recent_changes.append(change)

      if len(recent_changes) == 4:
        history = tuple(recent_changes)
        if history not in sequences_changed_for_this_secret:
          sequences[history] = sequences.get(history, 0) + price # update master dict for sequences
          sequences_changed_for_this_secret.add(history)

  return max(sequences.values())

def transform(secret):
  def mix(secret, value):
    return secret ^ value

  def prune(secret):
    bitmask = 0xFFFFFF # 16777216 == 2^24 = 0xFFFFFF
    return secret & bitmask # secret % 16777216 = secret & bitmask

  secret = prune(mix(secret, secret << 6)) # secret * 64 == secret << 6
  secret = prune(mix(secret, secret >> 5)) # secret // 32 == secret >> 5
  secret = prune(mix(secret, secret << 11)) # secret * 2048 == secret << 11
  return secret

if __name__ == "__main__":
  secrets = process_input()
  print(f"Part 1: {solve_part1(secrets)}")
  print(f"Part 2: {solve_part2(secrets)}")
