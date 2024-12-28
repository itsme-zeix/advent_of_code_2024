package main

import (
  "fmt"
  "os"
  "strings"
  "strconv"
  "sync"
  "time"
)

func process_input() map[int][]int {
  input, err := os.ReadFile("./day-07/input.txt")
  if err != nil {
    fmt.Println("Error in reading file: ", err)
    os.Exit(1)
  }

  lines := strings.Split(string(input), "\n")

  dict := map[int][]int{}
  for _, line := range lines {
    items := strings.Split(line, " ")

    result, err := strconv.Atoi(items[0][:len(items[0]) - 1])
    if err != nil {
      fmt.Println("Error in converting result to string: ", err)
      os.Exit(1)
    }

    operands := make([]int, len(items[1:]))
    for i, operandStr := range items[1:] {
      operand, err := strconv.Atoi(operandStr)
      if err != nil {
        fmt.Println("Error in converting operand to string: ", err)
        os.Exit(1)
      }
      operands[i] = operand
    }

    dict[result] = operands
  }

  return dict
}

func solve(hasConcat bool) int {
  resultToOperands := process_input()

  total := 0
  var wg sync.WaitGroup
  var mu sync.Mutex
  
  for result, operands := range resultToOperands {
    wg.Add(1)

    go func(result int, operands []int) {
      defer wg.Done()

      if helper(result, operands[0], operands, 1, hasConcat) {
        mu.Lock()
        total += result 
        mu.Unlock()
      }
    }(result, operands)
  }

  wg.Wait()
  return total
}

func helper(target int, curr int, operands []int, i int, hasConcat bool) bool {
  if curr == target && i == len(operands) {
    return true
  }
  if i >= len(operands) || curr > target {
    return false
  }
  operand := operands[i]
  plus := helper(target, curr + operand, operands, i + 1, hasConcat)
  mult := helper(target, curr * operand, operands, i + 1, hasConcat)
  concat := false
  if hasConcat {
    factor := 1
    for operand/factor > 0 {
      factor *= 10
    }
    concat = helper(target, curr * factor + operand, operands, i + 1, hasConcat)
  }
  return plus || mult || concat
}

func main() {
  start := time.Now()
  fmt.Println("Part 1:", solve(false))
  fmt.Println("Part 2:", solve(true))
  fmt.Println("Total time for both parts:", time.Since(start))
}
