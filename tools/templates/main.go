package main

import (
	"flag"
	"fmt"
	"os"

	"advent_of_code/jogtrot"
)

func SolveFirstPart(filepath string) {
	solution := fmt.Sprintf("Unimplemented. No solution for %s", filepath)
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	solution := fmt.Sprintf("Unimplemented. No solution for %s", filepath)
	jogtrot.PrintSolution(2, solution)
}

func main() {
	var part, input string

	flag.StringVar(&part, "p", "", "Puzzle part to solve")
	flag.StringVar(&input, "i", "./input.txt", "File with puzzle input")
	flag.Parse()

	if _, err := os.Stat(input); err != nil {
		panic(err)
	}

	parts := make([]string, 0)
	switch part {
	case "1", "2":
		parts = append(parts, part)
	default:
		parts = append(parts, "1", "2")
	}

	for _, part := range parts {
		switch part {
		case "1":
			SolveFirstPart(input)
		case "2":
			SolveSecondPart(input)
		}
	}
}
