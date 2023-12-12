package jogtrot

import "golang.org/x/exp/constraints"

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

func (m Matrix[_]) Height() int {
	return m.Shape.Y
}

func (m Matrix[_]) Width() int {
	return m.Shape.X
}

func RavelIndex2d(c Coordinate2d, shape Shape2d) int {
	return c.Y*shape.X + c.X
}

func UnravelIndex2d(index int, shape Shape2d) Coordinate2d {
	return Coordinate2d{X: index % shape.X, Y: index / shape.X}
}

func (c Coordinate2d) Translate(t Coordinate2d) Coordinate2d {
	return Coordinate2d{X: c.X + t.X, Y: c.Y + t.Y}
}

func (c Coordinate2d) IsWithinBounds(s Shape2d) bool {
	return c.X >= 0 && c.X < s.X && c.Y >= 0 && c.Y < s.Y
}
