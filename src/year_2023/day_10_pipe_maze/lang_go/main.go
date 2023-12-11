package main

import (
	"fmt"
	"slices"

	"advent_of_code/jogtrot"

	"golang.org/x/exp/constraints"
)

type Tuple2d[T any] struct {
	X, Y T
}

type (
	Shape2d      Tuple2d[int]
	Coordinate2d Tuple2d[int]
)

type Matrix[T constraints.Integer | constraints.Float | rune | byte] struct {
	Data  []T
	Shape Shape2d
}

func (m Matrix[T]) At(c Coordinate2d) T {
	return m.Data[RavelIndex2d(c, m.Shape)]
}

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

func (c Coordinate2d) Translate(t Coordinate2d) Coordinate2d {
	return Coordinate2d{X: c.X + t.X, Y: c.Y + t.Y}
}

func (c Coordinate2d) IsWithinBounds(s Shape2d) bool {
	return c.X >= 0 && c.X < s.X && c.Y >= 0 && c.Y < s.Y
}

func (c Coordinate2d) Neighbors(s Shape2d) []Coordinate2d {
	out := []Coordinate2d{}
	for _, direction := range []Direction{North, South, West, East} {
		neighbor := c.Translate(direction.AsTranslation())
		if neighbor.IsWithinBounds(s) {
			out = append(out, neighbor)
		}
	}
	return out
}

func UnravelIndex2d(index int, shape Shape2d) Coordinate2d {
	return Coordinate2d{X: index % shape.X, Y: index / shape.X}
}

func RavelIndex2d(c Coordinate2d, shape Shape2d) int {
	return c.Y*shape.X + c.X
}

func (d Direction) AsTranslation() Coordinate2d {
	switch d {
	case North:
		return Coordinate2d{X: 0, Y: -1}
	case South:
		return Coordinate2d{X: 0, Y: 1}
	case West:
		return Coordinate2d{X: -1, Y: 0}
	case East:
		return Coordinate2d{X: 1, Y: 0}
	default:
		panic("unexpected direction")
	}
}

type (
	Map   = Matrix[Tile]
	Graph = map[Coordinate2d][]Coordinate2d
)

type Cycle struct {
	Start Coordinate2d
	Paths map[Coordinate2d]struct{}
}

func FindCycle(m Map) Cycle {
	graph := make(Graph)

	var startCoordinate Coordinate2d
	startOk := false

	for idx, char := range m.Data {
		tile := Tile(char)
		coordinate := UnravelIndex2d(idx, m.Shape)
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
		for _, neighbor := range startCoordinate.Neighbors(m.Shape) {
			if slices.Contains(graph[neighbor], startCoordinate) {
				graph[startCoordinate] = append(graph[startCoordinate], neighbor)
			}
		}
	}

	visits := make(map[Coordinate2d]struct{})
	dfs(startCoordinate, graph, &visits)

	return Cycle{Start: startCoordinate, Paths: visits}
}

func dfs(coordinate Coordinate2d, graph Graph, visits *map[Coordinate2d]struct{}) {
	(*visits)[coordinate] = struct{}{}

	for _, neighbor := range graph[coordinate] {
		if _, ok := (*visits)[neighbor]; !ok {
			dfs(neighbor, graph, visits)
		}
	}
}

func ReadPuzzle(filepath string) Map {
	rows := jogtrot.ReadFileRows(filepath)
	shape := Shape2d{X: len(rows[0]), Y: len(rows)}
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
		coordinate := UnravelIndex2d(idx, puzzle.Shape)
		if _, ok := cycle.Paths[coordinate]; ok {
			continue
		}

		intersectionCount := 0
		for x := 0; x < coordinate.X; x++ {
			cycleCoordinate := Coordinate2d{X: x, Y: coordinate.Y}
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
