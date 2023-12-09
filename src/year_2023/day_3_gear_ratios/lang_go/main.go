package main

import (
	"flag"
	"os"
	"regexp"
	"strconv"

	"advent_of_code/jogtrot"
)

const (
	NO_SYMBOL = '.'
	GEAR      = '*'
)

type Coordinate struct {
	X int
	Y int
}

type Schematic struct {
	Rows []string
}

func (s *Schematic) Height() int {
	return len(s.Rows)
}

func (s *Schematic) Width() int {
	return len(s.Rows[0])
}

func (s *Schematic) IsCoordinateValid(c Coordinate) bool {
	return c.X >= 0 && c.X < s.Width() && c.Y >= 0 && c.Y < s.Height()
}

type Number struct {
	Position   Coordinate
	DigitCount int
	Value      int
}

func ParseNumbersFromStr(str string, y int, re *regexp.Regexp) []Number {
	var numbers []Number
	for _, idxs := range re.FindAllStringIndex(str, -1) {
		lhs := idxs[0]
		rhs := idxs[1]

		value, err := strconv.Atoi(str[lhs:rhs])
		if err != nil {
			panic(err)
		}
		number := Number{
			Position:   Coordinate{X: lhs, Y: y},
			DigitCount: rhs - lhs,
			Value:      value,
		}
		numbers = append(numbers, number)
	}

	return numbers
}

func ListAdjacentCellCoordinates(number *Number, schematic *Schematic) []Coordinate {
	var cells []Coordinate
	var pos Coordinate

	pos.X = number.Position.X - 1
	pos.Y = number.Position.Y
	if schematic.IsCoordinateValid(pos) {
		cells = append(cells, pos)
	}

	pos.X = number.Position.X + number.DigitCount
	if schematic.IsCoordinateValid(pos) {
		cells = append(cells, pos)
	}

	for dX := -1; dX <= number.DigitCount; dX++ {
		pos.X = number.Position.X + dX
		pos.Y = number.Position.Y - 1
		if schematic.IsCoordinateValid(pos) {
			cells = append(cells, pos)
		}

		pos.Y = number.Position.Y + 1
		if schematic.IsCoordinateValid(pos) {
			cells = append(cells, pos)
		}
	}

	return cells
}

func ListAdjacentGearCoordinates(number *Number, schematic *Schematic) []Coordinate {
	var cells []Coordinate
	for _, pos := range ListAdjacentCellCoordinates(number, schematic) {
		if schematic.Rows[pos.Y][pos.X] == GEAR {
			cells = append(cells, pos)
		}
	}
	return cells
}

func IsPartNumber(number *Number, schematic *Schematic) bool {
	for _, pos := range ListAdjacentCellCoordinates(number, schematic) {
		if schematic.Rows[pos.Y][pos.X] != NO_SYMBOL {
			return true
		}
	}
	return false
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	schematic := Schematic{Rows: rows}

	re := regexp.MustCompile(`\d+`)

	numbers := jogtrot.SliceFlatten(
		jogtrot.SliceMapWithIndex(
			rows,
			func(str string, index int) []Number {
				return ParseNumbersFromStr(str, index, re)
			},
		),
	)

	solution := 0
	for _, number := range numbers {
		if IsPartNumber(&number, &schematic) {
			solution += number.Value
		}
	}

	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	schematic := Schematic{Rows: rows}

	re := regexp.MustCompile(`\d+`)
	numbers := jogtrot.SliceFlatten(
		jogtrot.SliceMapWithIndex(
			rows,
			func(str string, index int) []Number {
				return ParseNumbersFromStr(str, index, re)
			},
		),
	)

	gearToAdjacentNumbers := make(map[Coordinate][]Number)
	for _, number := range numbers {
		for _, pos := range ListAdjacentGearCoordinates(&number, &schematic) {
			gearToAdjacentNumbers[pos] = append(gearToAdjacentNumbers[pos], number)
		}
	}

	solution := int64(0)
	for _, numbers := range gearToAdjacentNumbers {
		if len(numbers) == 2 {
			solution += int64(numbers[0].Value) * int64(numbers[1].Value)
		}
	}

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
