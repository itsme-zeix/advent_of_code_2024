package main

import (
  "os"
  "fmt"
  "strings"
)

type Coord struct {
  X int;
  Y int;
}

func processInput() (map[rune][]Coord, int, int) {
  input, err := os.ReadFile("./day-08/input.txt")
  if err != nil {
    fmt.Println("Error when reading file:", err)
    os.Exit(1)
  }

  lines := strings.Split(string(input), "\n") 
  antennaMapping := map[rune][]Coord{}
  for y, line := range lines {
    for x, ch := range line {
      if ch == '.' {
        continue
      }
      antenna := rune(ch)
      coord := Coord{X: x, Y: y}
      antennaMapping[antenna] = append(antennaMapping[antenna], coord)
    }
  }
  rows := len(lines)
  cols := len(lines[0])
  return antennaMapping, rows, cols
}

func part1() int {
  antennaMapping, rows, cols := processInput()
  antinodes := map[Coord]bool{}

  for _, antennas := range antennaMapping {
    for _, a := range antennas {
      for _, b := range antennas {
        if a == b {
          continue
        }
        dx, dy := b.X - a.X, b.Y - a.Y
        antinode := Coord{X: b.X + dx, Y: b.Y + dy}
        if isInBounds(antinode, rows, cols) {
          antinodes[antinode] = true
        }
      }
    }
  }
  return len(antinodes)
}

func part2() int {
  antennaMapping, rows, cols := processInput()
  antinodes := map[Coord]bool{}

  for _, antennas := range antennaMapping {
    for _, a := range antennas {
      for _, b := range antennas {
        if a == b {
          continue
        }
        dx, dy := b.X - a.X, b.Y - a.Y
        mult := 0
        for {
          newX, newY := b.X + dx*mult, b.Y + dy*mult
          if !isInBounds(Coord{X: newX, Y: newY}, rows, cols) {
            break
          }
          antinodes[Coord{X: newX, Y: newY}] = true
          mult++
        }
      }
    }
  }
  return len(antinodes)
}

func isInBounds(coord Coord, rows int, cols int) bool {
  x, y := coord.X, coord.Y
  return x >= 0 && x < cols && y >= 0 && y < rows
}

func main() {
  fmt.Println(part1())
  fmt.Println(part2())
}
