package main

import (
  "fmt"
  "strings"
  "os"
)

func process_input() [][]int {
  input, err := os.ReadFile("./day-10/input.txt")
  if err != nil {
    fmt.Println("Error while reading file:", err)
    os.Exit(1)
  }
  lines := strings.Split(string(input), "\n")
  matrix := [][]int{}
  for _, line := range lines {
    newLine := []int{}
    for _, ch := range line {
      newLine = append(newLine, int(ch - '0'))
    }
    matrix = append(matrix, newLine)
  }
  return matrix
}

type Coord struct {
  X int
  Y int
}

func solve() (int, int){
  mat := process_input()

  zeros := []Coord{}
  for y, row := range mat {
    for x, num := range row {
      if num == 0 {
        zeros = append(zeros, Coord{X: x, Y: y})
      }
    }
  }

  part1, part2 := 0, 0
  for _, zero := range zeros {
    unique_nines := map[Coord]bool{}
    part2 += dfs(zero.X, zero.Y, 0, mat, unique_nines)
    part1 += len(unique_nines)
  }
  return part1, part2
}

func dfs(x, y, digit int, mat [][]int, unique_nines map[Coord]bool) int {
  if digit == 9 {
    unique_nines[Coord{X: x, Y: y}] = true
    return 1
  }

  total := 0
  if isValid(x, y + 1, mat) && mat[y + 1][x] == digit + 1 {
    total += dfs(x, y + 1, digit + 1, mat, unique_nines)
  }
  if isValid(x, y - 1, mat) && mat[y - 1][x] == digit + 1 {
    total += dfs(x, y - 1, digit + 1, mat, unique_nines)
  }
  if isValid(x - 1, y, mat) && mat[y][x - 1] == digit + 1 {
    total += dfs(x - 1, y, digit + 1, mat, unique_nines)
  }
  if isValid(x + 1, y, mat) && mat[y][x + 1] == digit + 1 {
    total += dfs(x + 1, y, digit + 1, mat, unique_nines)
  }
  
  return total
}

func isValid(x, y int, mat [][]int) bool {
  return 0 <= x && x < len(mat[0]) && 0 <= y && y < len(mat);
}

func main() {
  part1, part2 := solve()
  fmt.Println("Part 1:", part1)
  fmt.Println("Part 2:", part2)
}
