package main

import (
  "fmt"
  "os"
  "strings"
  "strconv"
  "time"
)

type Rule struct {
  X int
  Y int
}

func process_input() (map[Rule]bool, [][]int) {
  input, err := os.ReadFile("./day-05/input.txt")
  if err != nil {
    fmt.Println("Error reading file: ", err)
    os.Exit(1)
  }

  rulesAndUpdates := strings.Split(string(input), "\n\n")
  rulesString := rulesAndUpdates[0]
  updatesString := rulesAndUpdates[1]
  
  rules := map[Rule]bool{}
  updates := [][]int{}

  for _, ruleString := range strings.Split(rulesString, "\n") {
    parts := strings.Split(ruleString, "|")
    if len(parts) != 2 {
      fmt.Println("Parsing gone wrong, more than 2 items in rule string.")
      os.Exit(1)
    }

    x, xErr := strconv.Atoi(strings.TrimSpace(parts[0]))
    y, yErr := strconv.Atoi(strings.TrimSpace(parts[1]))
    if xErr != nil {
      fmt.Println("Error with converting x from string to int: ", xErr)
      os.Exit(1)
    }
    if yErr != nil {
      fmt.Println("Error with converting y from string to int: ", yErr)
      os.Exit(1)
    }

    rules[Rule{X: x, Y: y}] = true
  }

  for _, updateString := range strings.Split(updatesString, "\n") {
    stringUpdate := strings.Split(updateString, ",")
    intUpdates := []int{}
    for _, str := range stringUpdate {
      num, err := strconv.Atoi(strings.TrimSpace(str))
      if err != nil {
        fmt.Println("Error converting update string to int: ", str)
        os.Exit(1)
      }
      intUpdates = append(intUpdates, num)
    }
    updates = append(updates, intUpdates)
  }
  
  return rules, updates
}


func solvePart1(rules map[Rule]bool, updates [][]int) int {
  total := 0
  for _, update := range updates {
    if isAllowed(rules, update) {
      middle_number := update[len(update) / 2]
      total += middle_number
    }
  }
  return total
}

func isAllowed(rules map[Rule]bool, update []int) bool {
  for i := 0; i < len(update); i++ {
    for j := i + 1; j < len(update); j++ {
      rule := Rule{X: update[i], Y: update[j]}
      _, exists := rules[rule]
      if !exists {
        return false
      }
    }
  }
  return true
}

func solvePart2(rules map[Rule]bool, updates [][]int, part1Solution int) int {
  total := 0
  for _, update := range updates {
    fixed := false

    for !fixed {
      fixed = true
      for i := 0; i < len(update); i++ {
        for j := i + 1; j < len(update); j++ {
          rule := Rule{X: update[j], Y: update[i]}
          _, exists := rules[rule]
          if exists {
            update[j], update[i] = update[i], update[j]
            fixed = false // Another pass is needed as a swap was done
          }
        }
      }
    }
    middle_number := update[len(update) / 2]
    total += middle_number
  }
  return total - part1Solution
}

func main() {
  startProcessing := time.Now()
  rules, updates := process_input()
  elapsed := time.Since(startProcessing)
  fmt.Println("Processing time: ", elapsed)

  startPart1 := time.Now()
  part1Solution := solvePart1(rules, updates)
  fmt.Println("Part 1 solution: ", part1Solution)
  elapsed = time.Since(startPart1)
  fmt.Println("Part 1 took: ", elapsed)

  startPart2 := time.Now()
  fmt.Println("Part 2 solution: ", solvePart2(rules, updates, part1Solution))
  elapsed = time.Since(startPart2)
  fmt.Println("Part 2 took: ", elapsed)
}
