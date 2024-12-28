package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"
)

type State struct {
  X int
  Y int
  DIR string
}

type Coord struct {
  X int
  Y int
}

func processInput() ([][]byte, State) {
  input, err := os.ReadFile("./day-06/input.txt")
  if err != nil {
    fmt.Println("Error reading file: ", err)
    os.Exit(1)
  }

  lines := strings.Split(string(input), "\n")
  var mat [][]byte
  for _, line := range lines {
      mat = append(mat, []byte(line))
  }
  
  var start State;
  for y, row := range mat {
    for x, cell := range row {
      if cell == '^' {
        start = State{X: x, Y: y, DIR: "UP"}
      }
    }
  }
  return mat, start
}

func part1() (map[Coord]bool, int) {
  mat, curr := processInput()
  visited := map[Coord]bool{}

  for true {
    if hasExited(mat, curr) {
      return visited, len(visited)
    }

    visited[Coord{X: curr.X, Y: curr.Y}] = true
    
    if metObstacle(mat, curr) {
      curr = turnRight(curr)
    } else {
      curr = move(curr)
    }
  }
  
  return visited, -1
}

func turnRight(curr State) State {
  turns := map[string]string{
    "UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP",
  }
  curr.DIR = turns[curr.DIR]
  return curr
}

func move(curr State) State {
  if curr.DIR == "UP" {
    curr.Y -= 1
  } else if curr.DIR == "DOWN" {
    curr.Y += 1
  } else if curr.DIR == "LEFT" {
    curr.X -= 1
  } else if curr.DIR == "RIGHT" {
    curr.X += 1
  }
  return curr
}

func metObstacle(mat [][]byte, curr State) bool {
  curr = move(curr)
  return !hasExited(mat, curr) && mat[curr.Y][curr.X] == '#'
}

func hasExited(mat [][]byte, curr State) bool {
  rows := len(mat)
  cols := len(mat[0])
  return curr.X < 0 || curr.X >= cols || curr.Y < 0 || curr.Y >= rows
}

func part2(possibleObstacles map[Coord]bool) int {
  // All possible obstacles we can add are the visited coords
  // in part 1.
  mat, curr := processInput()
  loopsFound := 0
  var mu sync.Mutex
  var wg sync.WaitGroup


  for obstacle := range possibleObstacles {
    wg.Add(1)
    go func(obstacle Coord) {
      defer wg.Done()

      matCopy := make([][]byte, len(mat))
      for i := range mat {
        matCopy[i] = append([]byte{}, mat[i]...)
      }

      matCopy[obstacle.Y][obstacle.X] = '#'
      if hasLoop(matCopy, curr) {
        mu.Lock()
        loopsFound++
        mu.Unlock()
      }
    }(obstacle)
  }

  wg.Wait()
  return loopsFound
}

func hasLoop(mat [][]byte, curr State) bool {
  visited := map[State]bool{}

  for true {
    if hasExited(mat, curr) {
      break
    }

    if visited[curr] {
      return true
    }
    visited[curr] = true

    if metObstacle(mat, curr) {
      curr = turnRight(curr) 
    } else {
      curr = move(curr)
    }
  }

  return false
}

func main() {
  start := time.Now()
  part1Visited, part1Sol := part1()
  fmt.Println("Part 1 sol: ", part1Sol)
  fmt.Println("Part 1 time: ", time.Since(start))

  start = time.Now()
  fmt.Println("Part 2 sol: ", part2(part1Visited))
  fmt.Println("Part 2 time: ", time.Since(start))
}
