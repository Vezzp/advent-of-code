package main

import (
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

func ReadContraptionFromFile(filepath string) Contraption {
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
	return contraption
}

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

	visitedCoords := map[jogtrot.Coordinate2d]struct{}{}
	for beam := range visitedBeams {
		visitedCoords[beam.Coordinate] = struct{}{}
	}

	return len(visitedCoords)
}

func SolveFirstPart(filepath string) {
	startBeam := Beam{Coordinate: jogtrot.Coordinate2d{X: 0, Y: 0}, Direction: jogtrot.East}
	solution := EnergizeContraption(ReadContraptionFromFile(filepath), startBeam)
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	contraption := ReadContraptionFromFile(filepath)
	borderCoordinates := make([]jogtrot.Coordinate2d, 0, 2*(contraption.Height()+contraption.Width()))
	for _, y := range []int{0, contraption.Shape.Y - 1} {
		for x := 0; x < contraption.Shape.X; x++ {
			borderCoordinates = append(borderCoordinates, jogtrot.Coordinate2d{X: x, Y: y})
		}
	}
	for _, x := range []int{0, contraption.Shape.X - 1} {
		for y := 1; y < contraption.Shape.Y-1; y++ {
			borderCoordinates = append(borderCoordinates, jogtrot.Coordinate2d{X: x, Y: y})
		}
	}

	solution := 0
	for _, coordinate := range borderCoordinates {
		directions := []jogtrot.Direction{}
		switch coordinate.X {
		case 0:
			directions = append(directions, jogtrot.East)
		case contraption.Shape.X - 1:
			directions = append(directions, jogtrot.West)
		}

		switch coordinate.Y {
		case 0:
			directions = append(directions, jogtrot.South)
		case contraption.Shape.Y - 1:
			directions = append(directions, jogtrot.North)
		}

		for _, direction := range directions {
			startBeam := Beam{Coordinate: coordinate, Direction: direction}
			solution = max(solution, EnergizeContraption(contraption, startBeam))
		}
	}

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
