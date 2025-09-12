package main

import (
	"fmt"

	"aoc/elf"
)

func SolveFirstPart(filepath string) {
	solution := fmt.Sprintf("Unimplemented. No solution for %s", filepath)
	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	solution := fmt.Sprintf("Unimplemented. No solution for %s", filepath)
	elf.PrintSolution(2, solution)
}

func main() {
	parts, input := elf.ParseCommandLine()
	for _, part := range parts {
		switch part {
		case "1":
			SolveFirstPart(input)
		case "2":
			SolveSecondPart(input)
		}
	}
}
