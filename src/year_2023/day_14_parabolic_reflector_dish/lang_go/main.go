package main

import (
	"fmt"
	"slices"
	"sort"
	"strconv"
	"strings"

	"advent_of_code/jogtrot"
)

const (
	RoundedRockSpace rune = 'O'
	EmptySpace       rune = '.'
)

type (
	Platform = jogtrot.Matrix[rune]
	Rock     = jogtrot.Coordinate2d
)

func NewPlatform(rows []string) Platform {
	out := Platform{}
	data := make([]rune, 0, len(rows)*len(rows[0]))
	for _, row := range rows {
		data = append(data, []rune(row)...)
	}
	out.Data = data
	out.Shape = jogtrot.Shape2d{X: len(rows[0]), Y: len(rows)}
	return out
}

func MoveRock(p *Platform, r *Rock, d jogtrot.Direction) {
	for {
		c := r.Translate(d.AsTranslation())
		if !c.IsWithinBounds(p.Shape) || p.At(c) != EmptySpace {
			break
		}
		*p.At_(*r) = EmptySpace
		r.X = c.X
		r.Y = c.Y
		*p.At_(*r) = RoundedRockSpace
	}
}

func RunMovementCycle(p *Platform, rocks []Rock) {
	for _, direction := range []jogtrot.Direction{
		jogtrot.North, jogtrot.West, jogtrot.South, jogtrot.East,
	} {
		sort.Slice(
			rocks,
			func(lidx, ridx int) bool {
				switch direction {
				case jogtrot.North:
					return rocks[lidx].Y < rocks[ridx].Y
				case jogtrot.West:
					return rocks[lidx].X < rocks[ridx].X
				case jogtrot.South:
					return rocks[lidx].Y > rocks[ridx].Y
				case jogtrot.East:
					return rocks[lidx].X > rocks[ridx].X
				default:
					panic(fmt.Sprintf("unexpected direction %s", direction))
				}
			},
		)

		for i := 0; i < len(rocks); i++ {
			MoveRock(p, &rocks[i], direction)
		}
	}
}

func ResolveRockConfigurationInvariant(p Platform, rocks []Rock) string {
	coordinates := make([]int, 0, len(rocks))
	for _, rock := range rocks {
		coordinates = append(coordinates, jogtrot.RavelIndex2d(rock, p.Shape))
	}
	slices.Sort(coordinates)
	out := strings.Join(
		jogtrot.SliceMap(coordinates, func(i int) string { return strconv.Itoa(i) }),
		"",
	)
	return out
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	platform := NewPlatform(rows)
	roundedRocks := []Rock{}
	for i, space := range platform.Data {
		if space == RoundedRockSpace {
			roundedRocks = append(roundedRocks, Rock(jogtrot.UnravelIndex2d(i, platform.Shape)))
		}
	}

	solution := 0
	for _, rock := range roundedRocks {
		MoveRock(&platform, &rock, jogtrot.North)
		solution += platform.Shape.Y - rock.Y
	}

	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	platform := NewPlatform(rows)
	roundedRocks := []Rock{}
	for i, space := range platform.Data {
		if space == RoundedRockSpace {
			roundedRocks = append(roundedRocks, Rock(jogtrot.UnravelIndex2d(i, platform.Shape)))
		}
	}

	invariants := map[string]int{}
	var (
		loopPeriod int
		numCycles  = 1000000000000
	)
	for i := 0; i <= numCycles; i++ {
		newInvariant := ResolveRockConfigurationInvariant(platform, roundedRocks)
		if loopStart, ok := invariants[newInvariant]; ok {
			loopPeriod = i - loopStart
			break
		}
		invariants[newInvariant] = i
		RunMovementCycle(&platform, roundedRocks)
	}

	for i := 0; i < (numCycles-len(invariants)-2)%loopPeriod; i++ {
		RunMovementCycle(&platform, roundedRocks)
	}

	solution := 0
	for _, rock := range roundedRocks {
		solution += platform.Shape.Y - rock.Y
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
