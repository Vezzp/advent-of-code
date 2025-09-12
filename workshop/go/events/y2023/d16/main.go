package main

import (
	"aoc/elf"
)

const (
	EmptySpace         rune = '.'
	VerticalSplitter   rune = '|'
	HorizontalSplitter rune = '-'
	SlashMirror        rune = '/'
	BackslashMirror    rune = '\\'
)

type Beam struct {
	Coordinate elf.Coordinate2d
	Direction  elf.Direction
}

func (b Beam) DefaultMove() Beam {
	return b.MoveDirection(b.Direction)
}

func (b Beam) MoveDirection(d elf.Direction) Beam {
	return Beam{
		Coordinate: b.Coordinate.Translate(d.AsTranslation()),
		Direction:  d,
	}
}

type Contraption = elf.Matrix[rune]

func EvolveBeam(beam Beam, contraption Contraption) []Beam {
	srcIdx := elf.RavelIndex2d(beam.Coordinate, contraption.Shape)
	srcRune := contraption.Data[srcIdx]

	out := []Beam{}
	switch srcRune {
	case EmptySpace:
		out = append(out, beam.DefaultMove())

	case VerticalSplitter:
		switch beam.Direction {
		case elf.North, elf.South:
			out = append(out, beam.DefaultMove())
		case elf.East, elf.West:
			out = append(out, beam.MoveDirection(elf.North), beam.MoveDirection(elf.South))
		}

	case HorizontalSplitter:
		switch beam.Direction {
		case elf.East, elf.West:
			out = append(out, beam.DefaultMove())
		case elf.North, elf.South:
			out = append(out, beam.MoveDirection(elf.East), beam.MoveDirection(elf.West))
		}

	case SlashMirror:
		switch beam.Direction {
		case elf.North:
			out = append(out, beam.MoveDirection(elf.East))
		case elf.South:
			out = append(out, beam.MoveDirection(elf.West))
		case elf.East:
			out = append(out, beam.MoveDirection(elf.North))
		case elf.West:
			out = append(out, beam.MoveDirection(elf.South))
		}

	case BackslashMirror:
		switch beam.Direction {
		case elf.North:
			out = append(out, beam.MoveDirection(elf.West))
		case elf.South:
			out = append(out, beam.MoveDirection(elf.East))
		case elf.East:
			out = append(out, beam.MoveDirection(elf.South))
		case elf.West:
			out = append(out, beam.MoveDirection(elf.North))
		}
	}

	return out
}

func EnergizeContraption(contraption Contraption, startBeam Beam) int {
	visitedBeams := map[Beam]struct{}{startBeam: {}}
	beams := []Beam{startBeam}

	for len(beams) != 0 {
		newBeams := []Beam{}
		for _, beam := range beams {
			for _, newBeam := range EvolveBeam(beam, contraption) {
				if !newBeam.Coordinate.IsWithinBounds(contraption.Shape) {
					continue
				}
				if _, ok := visitedBeams[newBeam]; ok {
					continue
				}
				newBeams = append(newBeams, newBeam)
				visitedBeams[newBeam] = struct{}{}
			}
		}
		beams = newBeams
	}

	visitedCoords := map[elf.Coordinate2d]struct{}{}
	for beam := range visitedBeams {
		visitedCoords[beam.Coordinate] = struct{}{}
	}

	return len(visitedCoords)
}

func SolveFirstPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	contraption := Contraption(elf.NewRuneMatrixFromRows(rows))
	startBeam := Beam{Coordinate: elf.Coordinate2d{X: 0, Y: 0}, Direction: elf.East}
	solution := EnergizeContraption(contraption, startBeam)
	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	contraption := Contraption(elf.NewRuneMatrixFromRows(rows))
	borderCoordinates := make([]elf.Coordinate2d, 0, 2*(contraption.Height()+contraption.Width()))
	for _, y := range []int{0, contraption.Shape.Y - 1} {
		for x := 0; x < contraption.Shape.X; x++ {
			borderCoordinates = append(borderCoordinates, elf.Coordinate2d{X: x, Y: y})
		}
	}
	for _, x := range []int{0, contraption.Shape.X - 1} {
		for y := 1; y < contraption.Shape.Y-1; y++ {
			borderCoordinates = append(borderCoordinates, elf.Coordinate2d{X: x, Y: y})
		}
	}

	solution := 0
	for _, coordinate := range borderCoordinates {
		directions := []elf.Direction{}
		switch coordinate.X {
		case 0:
			directions = append(directions, elf.East)
		case contraption.Shape.X - 1:
			directions = append(directions, elf.West)
		}

		switch coordinate.Y {
		case 0:
			directions = append(directions, elf.South)
		case contraption.Shape.Y - 1:
			directions = append(directions, elf.North)
		}

		for _, direction := range directions {
			startBeam := Beam{Coordinate: coordinate, Direction: direction}
			solution = max(solution, EnergizeContraption(contraption, startBeam))
		}
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
