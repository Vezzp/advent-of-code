package main

import (
	"fmt"
	"slices"

	"advent_of_code/jogtrot"

	"golang.org/x/exp/constraints"
)

type Tuple2d[T any] struct {
	X T
	Y T
}

type (
	Shape2d      = Tuple2d[int]
	Coordinate2d Tuple2d[int]
)

type Matrix[T constraints.Integer | constraints.Float | rune | byte] struct {
	Data  []T
	Shape Shape2d
}

func (m Matrix[_]) Height() int {
	return m.Shape.Y
}

func (m Matrix[_]) Width() int {
	return m.Shape.X
}

func (m Matrix[_]) Size() int {
	return m.Shape.X * m.Shape.Y
}

type (
	Vertex    = int
	Graph     = map[Vertex][]Vertex
	Adjacency int
	Color     uint8
)

const (
	White Color = iota
	Grey
	Black
)

func (c Coordinate2d) Translate(t Coordinate2d) Coordinate2d {
	return Coordinate2d{
		X: c.X + t.X,
		Y: c.Y + t.Y,
	}
}

func (c Coordinate2d) IsOutOfBounds() bool {
	return c.X < 0 || c.Y < 0
}

func UnravelIndex2d(index int, shape Shape2d) Coordinate2d {
	return Coordinate2d{
		X: index % shape.X,
		Y: index / shape.X,
	}
}

func RavelIndex2d(c Coordinate2d, shape Shape2d) int {
	return c.Y*shape.X + c.X
}

const (
	N Adjacency = iota
	S
	W
	E
)

func (a Adjacency) AsTranslation() Coordinate2d {
	switch a {
	case N:
		return Coordinate2d{X: 0, Y: -1}
	case S:
		return Coordinate2d{X: 0, Y: 1}
	case W:
		return Coordinate2d{X: -1, Y: 0}
	case E:
		return Coordinate2d{X: 1, Y: 0}
	default:
		panic("unexpected adjacency")
	}
}

type Map = Matrix[rune]

type Maze struct {
	Map   Map
	Start Coordinate2d
	Graph Graph
}

func NewMaze(m Map) Maze {
	graph := make(Graph)
	var start Coordinate2d
	startOk := false

	for idx, char := range m.Data {
		adjacencies := []Adjacency{}
		coordinate := UnravelIndex2d(idx, m.Shape)

		switch char {
		case 'S':
			start = coordinate
			startOk = true
			continue
		case '.':
			continue
		case '|':
			adjacencies = append(adjacencies, N, S)
		case '-':
			adjacencies = append(adjacencies, E, W)
		case 'L':
			adjacencies = append(adjacencies, N, E)
		case 'J':
			adjacencies = append(adjacencies, N, W)
		case '7':
			adjacencies = append(adjacencies, S, W)
		case 'F':
			adjacencies = append(adjacencies, S, E)
		}

		neighbors := graph[idx]
		for _, adjacency := range adjacencies {
			neighbor := coordinate.Translate(adjacency.AsTranslation())
			if neighbor.IsOutOfBounds() {
				continue
			}
			neighbors = append(neighbors, RavelIndex2d(neighbor, m.Shape))
		}
		graph[idx] = neighbors
	}

	if !startOk {
		panic("no start found")
	} else {
		idx := RavelIndex2d(start, m.Shape)
		neighbors := graph[idx]
		for _, adjacency := range []Adjacency{N, S, W, E} {
			neighbor := start.Translate(adjacency.AsTranslation())
			if neighbor.IsOutOfBounds() {
				continue
			}
			neighborIdx := RavelIndex2d(neighbor, m.Shape)
			if slices.Contains(graph[neighborIdx], idx) {
				neighbors = append(neighbors, neighborIdx)
			}
		}

		graph[idx] = neighbors
	}

	return Maze{
		Map:   m,
		Start: start,
		Graph: graph,
	}
}

func FindMaxCycleStepIndex(m Maze) int {
	colors := make([]Color, m.Map.Size())
	out := dfsMaxCycleStepIndex(RavelIndex2d(m.Start, m.Map.Shape), m.Graph, &colors, 0)

	return out
}

func dfsMaxCycleStepIndex(v Vertex, g Graph, colors *[]Color, length int) int {
	(*colors)[v] = Grey
	for _, neighbor := range g[v] {
		switch (*colors)[neighbor] {
		case White:
			length = max(length, dfsMaxCycleStepIndex(neighbor, g, colors, length+1))
		}
	}
	return length
}

func ReadMap(filepath string) Map {
	rows := jogtrot.ReadFileRows(filepath)
	shape := Shape2d{X: len(rows[0]), Y: len(rows)}
	data := make([]rune, 0, len(rows)*len(rows[0]))
	for _, row := range rows {
		data = append(data, []rune(row)...)
	}
	out := Matrix[rune]{
		Shape: shape,
		Data:  data,
	}
	return Map(out)
}

func SolveFirstPart(filepath string) {
	mat := ReadMap(filepath)
	maze := NewMaze(mat)
	solution := (1 + FindMaxCycleStepIndex(maze)) / 2
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
