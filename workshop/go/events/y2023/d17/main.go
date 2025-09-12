package main

import (
	"aoc/elf"

	"github.com/emirpasic/gods/queues/priorityqueue"
	"github.com/emirpasic/gods/utils"
)

type Heatmap = elf.Matrix[int]

type VisitedCell struct {
	Coordinate         elf.Coordinate2d
	Direction          elf.Direction
	DirectionStepCount int
}

type PriorityState struct {
	VisitedCell
	HeatLoss int
}

func cmpStateByPriority(lhs, rhs any) int {
	out := utils.IntComparator(
		lhs.(PriorityState).HeatLoss,
		rhs.(PriorityState).HeatLoss,
	)
	if out != 0 {
		return out
	}

	out = utils.IntComparator(
		elf.ManhattanDistance2d(lhs.(PriorityState).Coordinate, elf.Coordinate2d{}),
		elf.ManhattanDistance2d(rhs.(PriorityState).Coordinate, elf.Coordinate2d{}),
	)
	if out != 0 {
		return out
	}

	return -utils.IntComparator(
		lhs.(PriorityState).DirectionStepCount,
		rhs.(PriorityState).DirectionStepCount,
	)
}

func ReadHeatmapFromFile(filepath string) Heatmap {
	rows := elf.ReadFileRows(filepath)
	heatmapRune := elf.NewRuneMatrixFromRows(rows)
	out := Heatmap{
		Data:  elf.SliceMap(heatmapRune.Data, func(r rune) int { return int(r - '0') }),
		Shape: heatmapRune.Shape,
	}
	return out
}

func Solve(filepath string, minDirectionStepCount int, maxDirectionStepCount int) int {
	heatmap := ReadHeatmapFromFile(filepath)

	src := elf.Coordinate2d{X: 0, Y: 0}
	dst := elf.Coordinate2d{X: heatmap.Shape.X - 1, Y: heatmap.Shape.Y - 1}

	queue := priorityqueue.NewWith(cmpStateByPriority)
	queue.Enqueue(PriorityState{
		VisitedCell: VisitedCell{
			Coordinate:         src,
			Direction:          elf.UndefinedDirection,
			DirectionStepCount: 0,
		},
		HeatLoss: 0,
	})

	solution := 0
	visited := make(map[VisitedCell]struct{})
	for !queue.Empty() {
		var currentPriorityState PriorityState
		if current, ok := queue.Dequeue(); ok {
			currentPriorityState = current.(PriorityState)
		} else {
			break
		}

		if currentPriorityState.Coordinate == dst &&
			currentPriorityState.DirectionStepCount >= minDirectionStepCount {
			solution = currentPriorityState.HeatLoss
			break
		}

		if _, ok := visited[currentPriorityState.VisitedCell]; ok {
			continue
		} else {
			visited[currentPriorityState.VisitedCell] = struct{}{}
		}

		if currentPriorityState.DirectionStepCount < maxDirectionStepCount &&
			currentPriorityState.Direction != elf.UndefinedDirection {
			if nextCoordinate := currentPriorityState.Coordinate.Translate(
				currentPriorityState.Direction.AsTranslation(),
			); nextCoordinate.IsWithinBounds(heatmap.Shape) {
				queue.Enqueue(PriorityState{
					VisitedCell: VisitedCell{
						Coordinate:         nextCoordinate,
						Direction:          currentPriorityState.Direction,
						DirectionStepCount: currentPriorityState.DirectionStepCount + 1,
					},
					HeatLoss: currentPriorityState.HeatLoss + heatmap.At(nextCoordinate),
				})
			}
		}

		if currentPriorityState.Direction == elf.UndefinedDirection ||
			currentPriorityState.DirectionStepCount >= minDirectionStepCount {
			for _, nextDirection := range []elf.Direction{
				elf.North, elf.South, elf.West, elf.East,
			} {
				if nextDirection == currentPriorityState.Direction ||
					nextDirection == currentPriorityState.Direction.Opposite() {
					continue
				}
				if nextCoordinate := currentPriorityState.Coordinate.Translate(
					nextDirection.AsTranslation(),
				); nextCoordinate.IsWithinBounds(heatmap.Shape) {
					queue.Enqueue(PriorityState{
						VisitedCell: VisitedCell{
							Coordinate:         nextCoordinate,
							Direction:          nextDirection,
							DirectionStepCount: 1,
						},
						HeatLoss: currentPriorityState.HeatLoss + heatmap.At(nextCoordinate),
					})
				}
			}
		}

	}

	return solution
}

func SolveFirstPart(filepath string) {
	solution := Solve(filepath, -1, 3)
	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	solution := Solve(filepath, 4, 10)
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
