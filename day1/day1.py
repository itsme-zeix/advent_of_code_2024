import os

def part1():
  sum_of_differences = 0
  ls_left = []
  ls_right = []

  with open("./input.txt", "r") as f:
    for line in f:
      left, right = line.split()
      ls_left.append(int(left))
      ls_right.append(int(right))

    ls_left.sort()
    ls_right.sort()

    for i in range(len(ls_left)):
      difference = abs(ls_left[i] - ls_right[i])
      sum_of_differences += difference

  return sum_of_differences


def part2():
  # Searching each number is O(n) unless we use binary search on a sorted list which is O(logn)
  # Sort and binary search: O(nlogn)
  # Brute force search: O(n^2), could also cache for speedup.
  # Since dataset is relatively small, I'm just going to brute force it.

  ls_left = []
  ls_right = []
  similarityScore = 0

  with open("./input.txt", "r") as f:
    for line in f:
      left, right = line.split()
      ls_left.append(int(left))
      ls_right.append(int(right))
    
  for l in ls_left:
    counter = 0
    for r in ls_right:
      if l == r:
        counter += 1
    similarityScore += l * counter

  return similarityScore

if __name__ == "__main__":
  print(part1())
  print(part2())