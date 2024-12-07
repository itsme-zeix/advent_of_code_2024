package main

import (
  "bufio"
  "fmt"
  "os"
  "sort"
  "strconv"
  "strings"
)

func process_input() ([]int, []int) {
  var lsLeft, lsRight []int

  file, err := os.Open("./day-01/input.txt")
  if err != nil {
    fmt.Errorf("Error opening file: ", err)
    return nil, nil
  }
  defer file.Close()
  
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    line := strings.TrimSpace(scanner.Text())
    parts := strings.Fields(line)
    left, _ := strconv.Atoi(parts[0])
    right, _ := strconv.Atoi(parts[1])
    lsLeft = append(lsLeft, left)
    lsRight = append(lsRight, right)
  }
  if scanner.Err() != nil {
    fmt.Errorf("Error reading file: ", err) 
  }

  return lsLeft, lsRight
}

func solve_part1(lsLeft, lsRight []int) int {
  var sumOfDifferences int = 0
  sort.Ints(lsLeft)
  sort.Ints(lsRight)

  for i := 0; i < len(lsLeft); i++ {
    var difference int = abs(lsLeft[i] - lsRight[i])
    sumOfDifferences += difference
  }
  return sumOfDifferences
}

func abs(x int) int {
  if x < 0 {
    return -x
  }
  return x
}

func solve_part2(lsLeft, lsRight []int) int {
  var rightCount = make(map[int] int)
  var similarityScore int = 0

  for _, value := range lsRight {
    rightCount[value] = rightCount[value] + 1
  }
  
  for _, value := range lsLeft {
    similarityScore += value * rightCount[value]
  }
  
  return similarityScore
}

func main() {
  var lsLeft, lsRight []int = process_input()
  fmt.Println("Part 1: ", solve_part1(lsLeft, lsRight))
  fmt.Println("Part 2: ", solve_part2(lsLeft, lsRight))
}
