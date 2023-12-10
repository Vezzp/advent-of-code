package main

import (
	"fmt"
	"slices"

	"advent_of_code/jogtrot"
)

type (
	Vertex    = int
	Graph     = map[Vertex][]Vertex
	Map       []string
	Adjacency int
	Color     uint8
)

const (
	White Color = iota
	Grey
	Black
)

const (
	N Adjacency = iota
	S
	W
	E
)

func (a Adjacency) AsTranslation() Coordinate {
	switch a {
	case N:
		return Coordinate{X: 0, Y: -1}
	case S:
		return Coordinate{X: 0, Y: 1}
	case W:
		return Coordinate{X: -1, Y: 0}
	case E:
		return Coordinate{X: 1, Y: 0}
	default:
		panic("unexpected adjacency")
	}
}

type Coordinate struct {
	X int
	Y int
}

func (c Coordinate) Translate(t Coordinate) Coordinate {
	return Coordinate{
		X: c.X + t.X,
		Y: c.Y + t.Y,
	}
}

func (c Coordinate) IsOutOfBounds() bool {
	return c.X < 0 || c.Y < 0
}

func (m Map) ConvertVertexToCoordinate(v Vertex) Coordinate {
	return Coordinate{X: v % m.Width(), Y: v / m.Width()}
}

func (m Map) ConvertCoordinateToVertex(c Coordinate) Vertex {
	return c.Y*m.Width() + c.X
}

func (m Map) Height() int {
	return len(m)
}

func (m Map) Width() int {
	return len(m[0])
}

func (m Map) Size() int {
	return m.Height() * m.Width()
}

type Maze struct {
	Map   Map
	Start Coordinate
	Graph Graph
}

func NewMaze(m Map) Maze {
	graph := make(Graph)
	var start Coordinate
	startOk := false

	for y, row := range m {
		for x, char := range row {
			adjacencies := []Adjacency{}
			coordinate := Coordinate{X: x, Y: y}

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

			vertex := m.ConvertCoordinateToVertex(coordinate)
			neighbors := graph[vertex]
			for _, adjacency := range adjacencies {
				neighbor := coordinate.Translate(adjacency.AsTranslation())
				if neighbor.IsOutOfBounds() {
					continue
				}
				neighbors = append(neighbors, m.ConvertCoordinateToVertex(neighbor))
			}
			graph[vertex] = neighbors
		}
	}

	if !startOk {
		panic("no start found")
	}

	{
		startVertex := m.ConvertCoordinateToVertex(start)
		startNeighbors := graph[startVertex]
		for _, adjacency := range []Adjacency{N, S, W, E} {
			neighbor := start.Translate(adjacency.AsTranslation())
			if neighbor.IsOutOfBounds() {
				continue
			}
			neighborNeighbors := graph[m.ConvertCoordinateToVertex(neighbor)]
			if slices.Contains(neighborNeighbors, startVertex) {
				startNeighbors = append(startNeighbors, m.ConvertCoordinateToVertex(neighbor))
			}
		}
		graph[startVertex] = startNeighbors
	}

	return Maze{
		Map:   m,
		Start: start,
		Graph: graph,
	}
}

func FindMaxCycleStepIndex(m Maze) int {
	colors := make([]Color, m.Map.Size())
	return dfsMaxCycleStepIndex(m.Map.ConvertCoordinateToVertex(m.Start), m.Graph, &colors, 0)
}

func dfsMaxCycleStepIndex(v Vertex, g Graph, colors *[]Color, length int) int {
	(*colors)[v] = Grey
	for _, neighbor := range g[v] {
		switch (*colors)[neighbor] {
		case White:
			length = max(length, dfsMaxCycleStepIndex(neighbor, g, colors, length+1))
		}
	}
	(*colors)[int(v)] = Black
	return length
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	maze := NewMaze(Map(rows))
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
