package main

import (
	"aoc/elf"
)

type Universe = elf.Matrix[rune]

func ReadUniverseFromFile(filepath string) Universe {
	rows := elf.ReadFileRows(filepath)
	shape := elf.Shape2d{X: len(rows[0]), Y: len(rows)}
	data := make([]rune, 0, shape.X*shape.Y)
	for _, row := range rows {
		data = append(data, []rune(row)...)
	}
	return Universe{Data: data, Shape: shape}
}

func Solve(filepath string, coefficient int) int64 {
	universe := ReadUniverseFromFile(filepath)

	expansion := elf.Tuple2d[[]bool]{
		X: elf.NewDefaultSlice(universe.Shape.X, true),
		Y: elf.NewDefaultSlice(universe.Shape.Y, true),
	}

	galaxies := []elf.Coordinate2d{}
	for idx, pixel := range universe.Data {
		coordinate := elf.UnravelIndex2d(idx, universe.Shape)
		if pixel == '#' {
			expansion.X[coordinate.X] = false
			expansion.Y[coordinate.Y] = false
			galaxies = append(galaxies, coordinate)
		}
	}

	solution := int64(0)
	numExpansions := int64(0)
	for lidx, lhs := range galaxies[:len(galaxies)-1] {
		for _, rhs := range galaxies[lidx:] {
			solution += int64(elf.ManhattanDistance2d(lhs, rhs))

			minX, maxX := elf.MinMax(lhs.X, rhs.X)
			for x := minX; x <= maxX; x++ {
				if expansion.X[x] {
					numExpansions += 1
				}
			}

			minY, maxY := elf.MinMax(lhs.Y, rhs.Y)
			for y := minY; y <= maxY; y++ {
				if expansion.Y[y] {
					numExpansions += 1
				}
			}
		}
	}
	solution += int64(numExpansions) * (int64(coefficient) - 1)

	return solution
}

func SolveFirstPart(filepath string) {
	solution := Solve(filepath, 2)
	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	solution := Solve(filepath, 1000000)
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
