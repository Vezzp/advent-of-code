package main

import (
	"flag"
	"os"

	"advent_of_code/jogtrot"
)

func SolveFirstPart(filepath string) {
	jogtrot.PrintSolution(1, "unimplemented ...")
}

func SolveSecondPart(filepath string) {
	jogtrot.PrintSolution(2, "unimplemented ...")
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
