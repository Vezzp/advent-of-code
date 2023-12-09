package main

import (
	"flag"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"

	"advent_of_code/jogtrot"
)

type Record []int

func (r Record) Diff() Record {
	out := Record{}
	for idx := 1; idx < len(r); idx++ {
		diff := r[idx] - r[idx-1]
		out = append(out, diff)
	}
	return out
}

func ParseRecordFromStr(s string) Record {
	return jogtrot.SliceMap(
		strings.Fields(s),
		func(s string) int {
			if out, err := strconv.Atoi(s); err != nil {
				panic(err)
			} else {
				return out
			}
		},
	)
}

func SolveFirstPart(filepath string) {
	rows, err := jogtrot.ReadFileRows(filepath)
	if err != nil {
		panic(err)
	}
	records := jogtrot.SliceMap(rows, ParseRecordFromStr)

	solution := 0
	for _, record := range records {
		placeholders := []int{jogtrot.SliceLast(record)}
		for !jogtrot.SliceAll(record, func(i int) bool { return i == 0 }) {
			record = record.Diff()
			placeholders = append(placeholders, jogtrot.SliceLast(record))
		}

		solution += jogtrot.SliceSum(placeholders)
	}

	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows, err := jogtrot.ReadFileRows(filepath)
	if err != nil {
		panic(err)
	}
	records := jogtrot.SliceMap(rows, ParseRecordFromStr)

	solution := 0
	for _, record := range records {
		placeholders := []int{record[0]}
		for !jogtrot.SliceAll(record, func(i int) bool { return i == 0 }) {
			record = record.Diff()
			placeholders = append(placeholders, record[0])
		}

		slices.Reverse(placeholders)
		solution += jogtrot.SliceReduce(
			placeholders,
			func(lhs, rhs int) int { return rhs - lhs },
		)
	}

	jogtrot.PrintSolution(2, solution)
}

func main() {
	var part string

	flag.StringVar(&part, "p", "Part to solve", "Part to solve")
	flag.Parse()

	parts := make([]string, 0)
	switch part {
	case "1", "2":
		parts = append(parts, part)
	default:
		parts = append(parts, "1", "2")
	}

	var src string
	args := flag.Args()
	switch len(args) {
	case 0:
		src = "./input.txt"
		if _, err := os.Stat(src); err != nil {
			panic("When no puzzle input is given, ./input.txt must exist")
		}

	case 1:
		src = args[0]
	default:
		panic(fmt.Sprintf("Solver accepts no or single puzzle files, got %d", len(args)))
	}

	for _, part := range parts {
		switch part {
		case "1":
			SolveFirstPart(src)
		case "2":
			SolveSecondPart(src)
		}
	}
}
