package main

import (
  "fmt"
  "os"
  "strings"
)

func processInput() []int {
  input, err := os.ReadFile("./day-09/input.txt");
  if err != nil {
    fmt.Println("Error while reading file:", err)
    os.Exit(1)
  }

  trimmedInput := strings.TrimSpace(string(input))

  expanded := []int{}
  for i, ascii := range trimmedInput {
    repeats := int(ascii - '0')
    num := i / 2

    if i % 2 == 0 {
      for k := 0; k < repeats; k++ {
        expanded = append(expanded, num)
      }
    } else {
      for k := 0; k < repeats; k++ {
        expanded = append(expanded, -1) // we use -1 to represent '.'
      }
    }
  }
  return expanded
}

func part1() int {
  parsed := processInput()

  // 2 pointer approach
  total := 0
 r := len(parsed) - 1
  for l, num := range parsed {
    if l > r {
      break // early exit
    }
    if num != -1 {
      total += l * num
    } else {
      for parsed[r] == -1 {
        r -= 1
      }
      total += l * parsed[r]
      r -= 1
    }
  }
  return total
}

type Group struct {
  start int
  end int
  len int
  num int
}

func part2() int {
  parsed := processInput()

  // Preprocess data
  dots := []*Group{} // Store pointer for easier mutation later
  nums := []*Group{}

  i := 0
  for i < len(parsed) {
    start := i
    num := parsed[i]
    // determine the ending index of the current character
    for i + 1 < len(parsed) && parsed[i+1] == num {
      i++
    } 

    if num == -1 {
      group := Group{start: start, end: i, len: i - start + 1, num: num}
      dots = append(dots, &group)
    } else {
      group := Group{start: start, end: i, len: i - start + 1, num: num}
      nums = append(nums, &group)
    }

    i++
  }

  // Reverse nums array
  for i := len(nums)/2-1; i >= 0; i-- {
    opp := len(nums)-1-i
    nums[i], nums[opp] = nums[opp], nums[i]
  }

  for _, numGrp := range nums {
    for _, slots := range dots {
      if numGrp.len > slots.len || numGrp.start < slots.start {
        continue
      }

      if slots.len == numGrp.len {
        numGrp.start = slots.start
        numGrp.end = slots.end
        slots.len = 0 // set length to 0 so slot can no longer be used
        break
      } else {
        numGrp.start = slots.start
        numGrp.end = slots.start + numGrp.len - 1
        slots.start += numGrp.len
        slots.len = slots.end - slots.start + 1
        break
      }
    }
  }

  total := 0
  for _, numGrp := range nums {
    for mult := numGrp.start; mult <= numGrp.end; mult++ {
      total += numGrp.num * mult
    }
  }
  return total
}

func main() {
  fmt.Println("Part 1:", part1())
  fmt.Println("Part 2:", part2())
}
