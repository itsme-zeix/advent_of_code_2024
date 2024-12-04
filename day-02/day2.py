def check_report(report):
  is_increasing = int(report[0]) < int(report[1])

  for i in range(1, len(report)):
    i1 = int(report[i - 1])
    i2 = int(report[i])
    diff = abs(i2 - i1)
    is_invalid_change = diff < 1 or diff > 3

    if (is_increasing and i1 > i2) or (not is_increasing and i1 < i2) or is_invalid_change:
      return (True, i - 1)
  return (False, -1)

def solve_part1():
  unsafe_counter = 0
  total_lines = 0
  problematic_reports = []
  problematic_indexes = []

  with open("./day-02/input.txt", "r") as f:
    for line in f:
      total_lines += 1
      report = line.split()
      is_report_problematic, index = check_report(report)
      if (is_report_problematic):
        unsafe_counter += 1
        problematic_reports.append(report)
        problematic_indexes.append(index)
  return problematic_reports, problematic_indexes, total_lines - unsafe_counter

def solve_part2(problematic_reports, problematic_indexes):
  # Safe if there is only 1 problematic level in a report.
  # Naive brute force: is to remove each level in a report and check if the report is still problematic.
  # -> Cost of checking updated report = cost of checking report * O(n) where n is the size of the report = O(n^2)

  # Slightly more optimized: Pass the index of the problematic level. Remove the problematic level or its surrounding levels, 
  # then check if the report is still problematic.
  # -> Cost of checking updated report = cost of checking report * O(1) = O(n)
  fixed_reports = 0
  for report, index in zip(problematic_reports, problematic_indexes):
    report1 = report[:index - 1] + report[index:] # excludes report[index - 1]
    report2 = report[:index] + report[index + 1:] # excludes report[index]
    report3 = report[:index + 1] + report[index + 2:] # excludes report[index + 1]
    
    if not check_report(report1)[0] or not check_report(report2)[0] or not check_report(report3)[0]:
      print(report1, report2, report3)
      fixed_reports += 1

  return part1_solution + fixed_reports

if __name__ == "__main__":
  problematic_reports, problematic_indexes, part1_solution = solve_part1()
  print(part1_solution)
  print(solve_part2(problematic_reports, problematic_indexes))