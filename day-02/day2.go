package main

import (
  "bufio"
  "fmt"
  "os"
  "strings"
  "strconv"
)

func process_input() [][]int {
  var result [][]int

  file, _ := os.Open("./day-02/input.txt")
  defer file.Close()

  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    line := strings.TrimSpace(scanner.Text())
    stringParts := strings.Fields(line)

    var intParts []int = make([]int, len(stringParts))
    for i, str := range stringParts {
      intParts[i], _ = strconv.Atoi(str)
    }
    result = append(result, intParts)
  }
  return result
}

func isSorted(ls []int) (bool, int) {
  if len(ls) <= 1 {
    return true, -1
  }

  var isSortDirectionReversed bool = ls[0] > ls[1]
  for i := 1; i < len(ls); i++ {
    value1 := ls[i - 1]
    value2 := ls[i]
    if isSortDirectionReversed {
      if value1 <= value2 {
        return false, i - 1
      }
    } else {
      if value1 >= value2 {
        return false, i - 1
      }
    }
  }
  
  return true, -1
}

func isDifferenceAcceptable(ls []int) (bool, int) {
  for i := 1; i < len(ls); i++ {
    difference := abs(ls[i] - ls[i - 1])
    if difference < 1 || difference > 3 {
      return false, i
    }
  }
  return true, -1
}

func abs(x int) int {
  if x < 0 {
    return -x
  }
  return x
}

func isReportProblematic(report []int) (bool, int) {
  isSorted, i1 := isSorted(report);
  isDifferenceAcceptable, i2 := isDifferenceAcceptable(report); 

  if !isSorted {
    return true, i1
  }
  if !isDifferenceAcceptable {
    return true, i2
  }
  return false, -1
}

func solvePart1(input [][]int) (int, [][]int, []int) {
  var total int = 0
  var problematicReports [][]int = make([][]int, 0)
  var problematicIndexes []int = make([]int, 0)

  for _, ls := range input {
    isReportProblematic, i := isReportProblematic(ls)
    if isReportProblematic {
      problematicReports = append(problematicReports, ls)
      problematicIndexes = append(problematicIndexes, i)
    } else {
      total += 1
    }
  }
  return total, problematicReports, problematicIndexes
}

func solvePart2(problematicReports [][]int, problematicIndexes []int, part1Solution int) int {
  if len(problematicReports) != len(problematicIndexes) {
    return -1
  }

  total := part1Solution
  for i := 0; i < len(problematicReports); i++ {
    var report []int = problematicReports[i]
    var index int = problematicIndexes[i]

    var fixedReports [][]int
    if index > 0 {
      reportCopy := make([]int, len(report))
      copy(reportCopy, report)
      fixedReport := append(reportCopy[:index - 1], reportCopy[index:]...)
      fixedReports = append(fixedReports, fixedReport)
    }
    if index < len(report) {
      reportCopy := make([]int, len(report))
      copy(reportCopy, report)
      fixedReport := append(reportCopy[:index], reportCopy[index + 1:]...)
      fixedReports = append(fixedReports, fixedReport)
    }
    if index + 1 < len(report) {
      reportCopy := make([]int, len(report))
      copy(reportCopy, report)
      fixedReport := append(reportCopy[:index + 1], reportCopy[index + 2:]...)
      fixedReports = append(fixedReports, fixedReport)
    }

    for _, fixedReport := range fixedReports {
      problematic, _ := isReportProblematic(fixedReport);
      if !problematic {
        total += 1
        break
      }
    }
  }
  return total
}

func main() {
  var input [][]int = process_input()
  part1Solution, problematicReports, problematicIndexes := solvePart1(input)
  fmt.Println("Part 1:", part1Solution)
  fmt.Println("Part 2:", solvePart2(problematicReports, problematicIndexes, part1Solution))
}
