package main

import (
	"fmt"

	"advent_of_code/jogtrot"
)

const (
	EmptySpace         rune = '.'
	VerticalSplitter   rune = '|'
	HorizontalSplitter rune = '-'
	SlashMirror        rune = '/'
	BackslashMirror    rune = '\\'
)

type Beam struct {
	Coordinate jogtrot.Coordinate2d
	Direction  jogtrot.Direction
}

func (b Beam) DefaultMove() Beam {
	return b.MoveDirection(b.Direction)
}

func (b Beam) MoveDirection(d jogtrot.Direction) Beam {
	return Beam{
		Coordinate: b.Coordinate.Translate(d.AsTranslation()),
		Direction:  d,
	}
}

type Contraption = jogtrot.Matrix[rune]

func EvolveBeam(beam Beam, contraption Contraption) []Beam {
	srcIdx := jogtrot.RavelIndex2d(beam.Coordinate, contraption.Shape)
	srcRune := contraption.Data[srcIdx]

	out := []Beam{}
	switch srcRune {
	case EmptySpace:
		out = append(out, beam.DefaultMove())

	case VerticalSplitter:
		switch beam.Direction {
		case jogtrot.North, jogtrot.South:
			out = append(out, beam.DefaultMove())
		case jogtrot.East, jogtrot.West:
			out = append(out, beam.MoveDirection(jogtrot.North), beam.MoveDirection(jogtrot.South))
		}

	case HorizontalSplitter:
		switch beam.Direction {
		case jogtrot.East, jogtrot.West:
			out = append(out, beam.DefaultMove())
		case jogtrot.North, jogtrot.South:
			out = append(out, beam.MoveDirection(jogtrot.East), beam.MoveDirection(jogtrot.West))
		}

	case SlashMirror:
		switch beam.Direction {
		case jogtrot.North:
			out = append(out, beam.MoveDirection(jogtrot.East))
		case jogtrot.South:
			out = append(out, beam.MoveDirection(jogtrot.West))
		case jogtrot.East:
			out = append(out, beam.MoveDirection(jogtrot.North))
		case jogtrot.West:
			out = append(out, beam.MoveDirection(jogtrot.South))
		}

	case BackslashMirror:
		switch beam.Direction {
		case jogtrot.North:
			out = append(out, beam.MoveDirection(jogtrot.West))
		case jogtrot.South:
			out = append(out, beam.MoveDirection(jogtrot.East))
		case jogtrot.East:
			out = append(out, beam.MoveDirection(jogtrot.South))
		case jogtrot.West:
			out = append(out, beam.MoveDirection(jogtrot.North))
		}
	}

	return out
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	contraption := Contraption(
		jogtrot.NewMatrixWithShape[rune](
			jogtrot.Shape2d{X: len(rows[0]), Y: len(rows)},
		),
	)
	for y, row := range rows {
		for x, ch := range row {
			idx := jogtrot.RavelIndex2d(jogtrot.Coordinate2d{X: x, Y: y}, contraption.Shape)
			contraption.Data[idx] = ch
		}
	}

	startBeam := Beam{Coordinate: jogtrot.Coordinate2d{X: 0, Y: 0}, Direction: jogtrot.East}
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

	visitedCoords := map[jogtrot.Coordinate2d]struct{}{}
	for beam := range visitedBeams {
		visitedCoords[beam.Coordinate] = struct{}{}
	}

	solution := len(visitedCoords)
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
