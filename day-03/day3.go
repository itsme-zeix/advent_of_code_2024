package main

import (
  "fmt"
  "os"
  "strings"
  "regexp"
  "strconv"
)

func process_input() string {
  input, _ := os.ReadFile("./day-03/input.txt")
  return strings.ReplaceAll(string(input), "\n", "")
}

func solve_part1(input string) int {
  var pattern string = `mul\((\d+),(\d+)\)`
  var re *regexp.Regexp = regexp.MustCompile(pattern)
  var matches [][]string = re.FindAllStringSubmatch(input, -1)

  var total int = 0
  for _, match := range matches {
    x, _ := strconv.Atoi(match[1])
    y, _ := strconv.Atoi(match[2])
    total += x * y
  }
  return total
}

func solve_part2(input string) int {
  var updatedInput string = "do()" + input + "don't()"
  var pattern string = `do\(\)(.*?)don\'t\(\)`
  var re *regexp.Regexp = regexp.MustCompile(pattern)
  var matches [][]string = re.FindAllStringSubmatch(updatedInput, -1)

  var total int = 0
  for _, match := range matches {
    total += solve_part1(match[1])
  }
  return total
}


func main() {
  input := process_input()
  fmt.Println("Part 1:", solve_part1(input))
  fmt.Println("Part 2:", solve_part2(input))
}
