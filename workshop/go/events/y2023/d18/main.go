package main

import (
	"fmt"
	"strconv"
	"strings"

	"aoc/elf"
)

type DigStep struct {
	Direction elf.Direction
	Count     int64
}

type InputStep struct {
	DigStep
	Color string
}

func ParseInputStepFromStr(str string) InputStep {
	parts := strings.Fields(str)

	var direction elf.Direction
	switch parts[0] {
	case "U":
		direction = elf.North
	case "D":
		direction = elf.South
	case "L":
		direction = elf.West
	case "R":
		direction = elf.East
	default:
		panic("Invalid direction")
	}

	var count int64
	if parsedCount, err := strconv.Atoi(parts[1]); err != nil {
		panic(err)
	} else {
		count = int64(parsedCount)
	}

	return InputStep{
		DigStep: DigStep{
			Direction: direction,
			Count:     count,
		},
		Color: parts[2][2 : len(parts[2])-1],
	}
}

func Solve(steps []DigStep) int64 {
	perimeter := int64(0)
	cornerCoordinates := []elf.Tuple2d[int64]{{}}
	for _, step := range steps {
		coordinate := elf.SliceLast(cornerCoordinates)
		switch step.Direction {
		case elf.East:
			coordinate.X += step.Count
		case elf.West:
			coordinate.X -= step.Count
		case elf.North:
			coordinate.Y += step.Count
		case elf.South:
			coordinate.Y -= step.Count
		}
		cornerCoordinates = append(cornerCoordinates, coordinate)
		perimeter += step.Count
	}

	area := int64(0)
	for idx := 0; idx < len(cornerCoordinates)-1; idx++ {
		lhs := cornerCoordinates[idx]
		rhs := cornerCoordinates[idx+1]
		area += (lhs.Y + rhs.Y) * (lhs.X - rhs.X)
	}
	area /= 2
	if area < 0 {
		area = -area
	}

	return area + perimeter/2 + 1
}

func SolveFirstPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	inputSteps := elf.SliceMap(rows, ParseInputStepFromStr)
	digSteps := elf.SliceMap(
		inputSteps,
		func(step InputStep) DigStep {
			return step.DigStep
		},
	)
	solution := Solve(digSteps)
	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	inputSteps := elf.SliceMap(rows, ParseInputStepFromStr)
	digSteps := elf.SliceMap(
		inputSteps,
		func(step InputStep) DigStep {
			count, err := strconv.ParseInt(step.Color[:len(step.Color)-1], 16, 64)
			if err != nil {
				panic(err)
			}
			var direction elf.Direction
			switch step.Color[len(step.Color)-1] {
			case '0':
				direction = elf.East
			case '1':
				direction = elf.South
			case '2':
				direction = elf.West
			case '3':
				direction = elf.North
			default:
				panic(fmt.Sprintf("Cannot infer direction from color %v", step))
			}
			return DigStep{
				Direction: direction,
				Count:     count,
			}
		},
	)
	solution := Solve(digSteps)
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
