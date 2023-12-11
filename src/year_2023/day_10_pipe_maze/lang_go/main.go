package main

import (
	"fmt"
	"slices"

	"advent_of_code/jogtrot"
)

type Direction rune

func (d Direction) String() string {
	return string(d)
}

const (
	North Direction = 'N'
	South Direction = 'S'
	West  Direction = 'W'
	East  Direction = 'E'
)

type Tile rune

func (t Tile) String() string {
	return string(t)
}

func (t Tile) Directions() []Direction {
	var out []Direction
	switch t {
	case '|':
		out = []Direction{North, South}
	case '-':
		out = []Direction{East, West}
	case 'L':
		out = []Direction{North, East}
	case 'J':
		out = []Direction{North, West}
	case '7':
		out = []Direction{South, West}
	case 'F':
		out = []Direction{South, East}
	default:
		panic(fmt.Sprintf("unexpected tile %s", t))
	}
	return out
}

const (
	Vertical   Tile = '|'
	Horizontal Tile = '-'
	DownLeft   Tile = 'L'
	RightUp    Tile = 'J'
	LeftDown   Tile = '7'
	UpRight    Tile = 'F'
	Ground     Tile = '.'
	Start      Tile = 'S'
)

func FindCoordinateNeighbors(coordinate jogtrot.Coordinate2d, shape jogtrot.Shape2d) []jogtrot.Coordinate2d {
	out := []jogtrot.Coordinate2d{}
	for _, direction := range []Direction{North, South, West, East} {
		neighbor := coordinate.Translate(direction.AsTranslation())
		if neighbor.IsWithinBounds(shape) {
			out = append(out, neighbor)
		}
	}
	return out
}

func (d Direction) AsTranslation() jogtrot.Coordinate2d {
	switch d {
	case North:
		return jogtrot.Coordinate2d{X: 0, Y: -1}
	case South:
		return jogtrot.Coordinate2d{X: 0, Y: 1}
	case West:
		return jogtrot.Coordinate2d{X: -1, Y: 0}
	case East:
		return jogtrot.Coordinate2d{X: 1, Y: 0}
	default:
		panic("unexpected direction")
	}
}

type (
	Map   = jogtrot.Matrix[Tile]
	Graph = map[jogtrot.Coordinate2d][]jogtrot.Coordinate2d
)

type Cycle struct {
	Start jogtrot.Coordinate2d
	Paths map[jogtrot.Coordinate2d]struct{}
}

func FindCycle(m Map) Cycle {
	graph := make(Graph)

	var startCoordinate jogtrot.Coordinate2d
	startOk := false

	for idx, char := range m.Data {
		tile := Tile(char)
		coordinate := jogtrot.UnravelIndex2d(idx, m.Shape)
		var directions []Direction

		switch tile {
		case Start:
			startCoordinate = coordinate
			startOk = true
			continue
		case Ground:
			continue
		default:
			directions = tile.Directions()
		}

		for _, direction := range directions {
			neighbor := coordinate.Translate(direction.AsTranslation())
			if neighbor.IsWithinBounds(m.Shape) {
				graph[coordinate] = append(graph[coordinate], neighbor)
			}

		}

	}

	if !startOk {
		panic("no start found")
	} else {
		for _, neighbor := range FindCoordinateNeighbors(startCoordinate, m.Shape) {
			if slices.Contains(graph[neighbor], startCoordinate) {
				graph[startCoordinate] = append(graph[startCoordinate], neighbor)
			}
		}
	}

	visits := make(map[jogtrot.Coordinate2d]struct{})
	dfs(startCoordinate, graph, &visits)

	return Cycle{Start: startCoordinate, Paths: visits}
}

func dfs(coordinate jogtrot.Coordinate2d, graph Graph, visits *map[jogtrot.Coordinate2d]struct{}) {
	(*visits)[coordinate] = struct{}{}

	for _, neighbor := range graph[coordinate] {
		if _, ok := (*visits)[neighbor]; !ok {
			dfs(neighbor, graph, visits)
		}
	}
}

func ReadPuzzle(filepath string) Map {
	rows := jogtrot.ReadFileRows(filepath)
	shape := jogtrot.Shape2d{X: len(rows[0]), Y: len(rows)}
	data := make([]Tile, 0, len(rows)*len(rows[0]))
	for _, row := range rows {
		data = append(data, []Tile(row)...)
	}
	out := Map{Shape: shape, Data: data}
	return Map(out)
}

func SolveFirstPart(filepath string) {
	puzzle := ReadPuzzle(filepath)
	cycle := FindCycle(puzzle)

	solution := (1 + len(cycle.Paths)) / 2
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	puzzle := ReadPuzzle(filepath)
	cycle := FindCycle(puzzle)

	solution := 0
	for idx := range puzzle.Data {
		coordinate := jogtrot.UnravelIndex2d(idx, puzzle.Shape)
		if _, ok := cycle.Paths[coordinate]; ok {
			continue
		}

		intersectionCount := 0
		for x := 0; x < coordinate.X; x++ {
			cycleCoordinate := jogtrot.Coordinate2d{X: x, Y: coordinate.Y}
			if _, ok := cycle.Paths[cycleCoordinate]; !ok {
				continue
			}

			switch puzzle.At(cycleCoordinate) {
			case Vertical, RightUp, DownLeft:
				intersectionCount++
			}
		}
		if intersectionCount%2 == 1 {
			solution += 1
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
