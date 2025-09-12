package main

import (
	"slices"
	"strconv"
	"strings"

	"aoc/elf"
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
	return elf.SliceMap(
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
	rows := elf.ReadFileRows(filepath)
	records := elf.SliceMap(rows, ParseRecordFromStr)

	solution := 0
	for _, record := range records {
		placeholders := []int{elf.SliceLast(record)}
		for !elf.SliceAll(record, func(i int) bool { return i == 0 }) {
			record = record.Diff()
			placeholders = append(placeholders, elf.SliceLast(record))
		}

		solution += elf.SliceSum(placeholders)
	}

	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	records := elf.SliceMap(rows, ParseRecordFromStr)

	solution := 0
	for _, record := range records {
		placeholders := []int{record[0]}
		for !elf.SliceAll(record, func(i int) bool { return i == 0 }) {
			record = record.Diff()
			placeholders = append(placeholders, record[0])
		}

		slices.Reverse(placeholders)
		solution += elf.SliceReduce(
			placeholders,
			func(lhs, rhs int) int { return rhs - lhs },
		)
	}

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
