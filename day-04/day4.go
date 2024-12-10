package main

import (
  "bufio"
  "os"
  "fmt"
  "strings"
)

type Direction struct {
  dx int
  dy int
}

func process_input() [][]rune {
  f, err := os.Open("./day-04/input.txt")
  if err != nil {
    fmt.Println("Error opening file:", err)
    os.Exit(1)
  }
  defer f.Close()

  var matrix [][]rune
  scanner := bufio.NewScanner(f)
  for scanner.Scan() {
    line := strings.TrimSpace(scanner.Text())
    row := []rune(line)
    matrix = append(matrix, row) 
    // Can be slightly optimized by preallocating memory for matrix, requiring 
    // a prior search of cost O(m) for an m*n matrix to determine no. of rows.
  }
  if err := scanner.Err(); err != nil {
    fmt.Println("Error reading file:", err)
    os.Exit(1)
  }
  return matrix
}

func solvePart1(matrix [][]rune) int {
  var noOfRows int = len(matrix)
  var noOfCols int = len(matrix[0])

  var directions []Direction = []Direction{
    {1, 0},
    {-1, 0},
    {0, 1},
    {0, -1},
    {1, 1},
    {-1, -1},
    {1, -1},
    {-1, 1},
  }

  var result int = 0
  for y := 0; y < noOfRows; y++ {
    for x := 0; x < noOfCols; x++ {
      if matrix[y][x] != 'X' {
        continue
      }

      for _, direction := range directions {
        result += checkPart1(matrix, x, y, direction, 1)
      }
    }
  }
  return result
}

func checkPart1(matrix [][]rune, x, y int, direction Direction, index int) int {
  var noOfRows int = len(matrix)
  var noOfCols int = len(matrix[0])
  var letters []rune = []rune{'X', 'M', 'A', 'S'}

  if index == len(letters) {
    return 1
  }

  nx, ny := x + direction.dx, y + direction.dy

  if isWithinLimit(nx, ny, noOfRows, noOfCols) && matrix[ny][nx] == letters[index] {
    return checkPart1(matrix, nx, ny, direction, index + 1)
  }
  return 0
}

func solvePart2(matrix [][]rune) int {
  var noOfRows int = len(matrix)
  var noOfCols int = len(matrix[0])

  var result int = 0
  for y := 0; y < noOfRows; y++ {
    for x := 0; x < noOfCols; x++ {
      if matrix[y][x] != 'A' {
        continue
      }

      diagonal1 := isWithinLimit(y + 1, x + 1, noOfRows, noOfCols) &&
                   isWithinLimit(y - 1, x - 1, noOfRows, noOfCols) &&
                   ((matrix[y + 1][x + 1] == 'M' && matrix[y - 1][x - 1] == 'S') ||
                    (matrix[y + 1][x + 1] == 'S' && matrix[y - 1][x - 1] == 'M'))
      diagonal2 := isWithinLimit(y + 1, x - 1, noOfRows, noOfCols) &&
                   isWithinLimit(y - 1, x + 1, noOfRows, noOfCols) &&
                   ((matrix[y + 1][x - 1] == 'M' && matrix[y - 1][x + 1] == 'S') ||
                    (matrix[y + 1][x - 1] == 'S' && matrix[y - 1][x + 1] == 'M'))

      if diagonal1 && diagonal2 {
        result++
      }
    }
  }
  return result
}

func isWithinLimit(x, y, noOfRows, noOfCols int) bool {
  return x >= 0 && x < noOfCols && y >= 0 && y < noOfRows
}

func main() {
  var matrix [][]rune = process_input()
  fmt.Println("Part 1 Solution: ", solvePart1(matrix))
  fmt.Println("Part 2 Solution: ", solvePart2(matrix))
}

