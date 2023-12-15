package main

import (
	"fmt"
	"strings"

	"advent_of_code/jogtrot"
)

func LensHash(s string) int {
	out := int64(0)
	for _, s := range s {
		out += int64(s)
		out *= 17
		out %= 256
	}
	return int(out)
}

func SolveFirstPart(filepath string) {
	row := jogtrot.ReadFileRows(filepath)[0]
	solution := 0
	for _, step := range strings.Split(row, ",") {
		solution += LensHash(step)
	}
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	solution := fmt.Sprintf("Unimplemented. No solution for %s", filepath)
	jogtrot.PrintSolution(2, solution)
}

func main() {
	parts, input := jogtrot.ParseCommandLine()
	for _, part := range parts {
		switch part {
		case "1":
			SolveFirstPart(input)
		case "2":
			SolveSecondPart(input)
		}
	}
}
