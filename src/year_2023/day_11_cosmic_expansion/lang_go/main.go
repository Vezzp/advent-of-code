package main

import (
	"fmt"

	"advent_of_code/jogtrot"
)

type Universe = jogtrot.Matrix[rune]

func ReadUniverseFromFile(filepath string) Universe {
	rows := jogtrot.ReadFileRows(filepath)
	shape := jogtrot.Shape2d{X: len(rows[0]), Y: len(rows)}
	data := make([]rune, 0, shape.X*shape.Y)
	for _, row := range rows {
		data = append(data, []rune(row)...)
	}
	return Universe{Data: data, Shape: shape}
}

func SolveFirstPart(filepath string) {
	universe := ReadUniverseFromFile(filepath)

	expansion := jogtrot.Tuple2d[[]bool]{
		X: jogtrot.NewDefaultSlice(universe.Shape.X, true),
		Y: jogtrot.NewDefaultSlice(universe.Shape.Y, true),
	}

	galaxies := []jogtrot.Coordinate2d{}
	for idx, pixel := range universe.Data {
		coordinate := jogtrot.UnravelIndex2d(idx, universe.Shape)
		if pixel == '#' {
			expansion.X[coordinate.X] = false
			expansion.Y[coordinate.Y] = false
			galaxies = append(galaxies, coordinate)
		}
	}

	solution := 0
	for lidx, lhs := range galaxies[:len(galaxies)-1] {
		for _, rhs := range galaxies[lidx:] {
			solution += jogtrot.ManhattanDistance2d(lhs, rhs)

			minX := lhs.X
			maxX := rhs.X
			if lhs.X > rhs.X {
				minX, maxX = rhs.X, lhs.X
			}
			for x := minX; x <= maxX; x++ {
				if expansion.X[x] {
					solution += 1
				}
			}

			minY := lhs.Y
			maxY := rhs.Y
			if lhs.Y > rhs.Y {
				minY, maxY = rhs.Y, lhs.Y
			}
			for y := minY; y <= maxY; y++ {
				if expansion.Y[y] {
					solution += 1
				}
			}
		}
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
