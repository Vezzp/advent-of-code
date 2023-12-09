package main

import (
	"flag"
	"fmt"
	"os"

	"advent_of_code/jogtrot"
)

type (
	Position  = string
	Network   = map[Position][2]Position
	Positions = []Position
)

const (
	U Direction = 'U'
	L Direction = 'L'
	R Direction = 'R'
)

type Direction byte

func (d Direction) String() string {
	return string(byte(d))
}

func (d Direction) Index() int {
	switch d {
	case L:
		return 0
	case R:
		return 1
	default:
		panic("unexpected direction")
	}
}

type DesertMap struct {
	Directions []Direction
	Network    Network
}

type Step struct {
	Start     Position
	End       Position
	Direction Direction
}

func (s Step) String() string {
	return fmt.Sprintf("%s %s %s", s.Start, s.Direction, s.End)
}

type Journey struct {
	Map              DesertMap
	Start            Position
	SuccessPredicate func(Position) bool

	StepCount int
	Position  Position
}

func NewJourney(desertMap DesertMap, startPosition Position, successPredicate func(Position) bool) *Journey {
	return &Journey{
		Map:              desertMap,
		Start:            startPosition,
		SuccessPredicate: successPredicate,
		StepCount:        0,
		Position:         startPosition,
	}
}

func (j *Journey) Success() bool {
	return j.SuccessPredicate(j.Position)
}

func (j *Journey) MakeStep() {
	var start Position
	if j.StepCount == 0 {
		start = j.Start
	} else {
		start = j.Position
	}
	direction := j.Map.Directions[j.StepCount%len(j.Map.Directions)]
	j.Position = j.Map.Network[start][direction.Index()]
	j.StepCount++
}

func ParseDesertMapFromFile(filepath string) DesertMap {
	rows := jogtrot.ReadFileRows(filepath)
	directions := rows[0]
	network := make(Network)
	var src, ldst, rdst string
	for _, row := range rows[2:] {
		if _, err := fmt.Sscanf(row, "%3s = (%3s, %3s)", &src, &ldst, &rdst); err != nil {
			panic(err)
		}
		network[src] = [2]string{ldst, rdst}
	}
	return DesertMap{
		Directions: []Direction(directions),
		Network:    network,
	}
}

func SolveFirstPart(filepath string) {
	desertMap := ParseDesertMapFromFile(filepath)
	journey := NewJourney(desertMap, Position("AAA"), func(p Position) bool { return p == "ZZZ" })

	for !journey.Success() {
		journey.MakeStep()
	}

	jogtrot.PrintSolution(1, journey.StepCount)
}

func SolveSecondPart(filepath string) {
	desertMap := ParseDesertMapFromFile(filepath)

	stepCounts := make([]int, 0)
	for start := range desertMap.Network {
		if start[len(start)-1] != 'A' {
			continue
		}
		journey := NewJourney(desertMap, start, func(p Position) bool { return p[len(p)-1] == 'Z' })
		for !journey.Success() {
			journey.MakeStep()
		}
		stepCounts = append(stepCounts, journey.StepCount)
	}

	solution := jogtrot.SliceReduce(stepCounts, jogtrot.LCM)
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
