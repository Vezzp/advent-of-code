package jogtrot

import "strings"

type Tuple2d[T any] struct {
	X, Y T
}

type (
	Shape2d      Tuple2d[int]
	Coordinate2d Tuple2d[int]
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

type Matrix[T any] struct {
	Data  []T
	Shape Shape2d
}

func (m Matrix[T]) Fill(t T) Matrix[T] {
	out := NewMatrixFromShape[T](m.Shape)
	out.Fill_(t)
	return out
}

func (m Matrix[T]) Fill_(t T) {
	for i := range m.Data {
		m.Data[i] = t
	}
}

func NewMatrixFromShape[T any](s Shape2d) Matrix[T] {
	return Matrix[T]{
		Data:  make([]T, s.X*s.Y),
		Shape: s,
	}
}

func (m Matrix[T]) At(c Coordinate2d) T {
	return m.Data[RavelIndex2d(c, m.Shape)]
}

func (m Matrix[T]) At_(c Coordinate2d) *T {
	return &m.Data[RavelIndex2d(c, m.Shape)]
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

func (c *Coordinate2d) Translate_(t Coordinate2d) {
	c.X += t.X
	c.Y += t.Y
}

func (c Coordinate2d) IsWithinBounds(s Shape2d) bool {
	return c.X >= 0 && c.X < s.X && c.Y >= 0 && c.Y < s.Y
}

func RuneMatrixStringer(m Matrix[rune]) string {
	var sb strings.Builder
	for y := 0; y < m.Shape.Y; y++ {
		for x := 0; x < m.Shape.X; x++ {
			sb.WriteRune(m.Data[RavelIndex2d(Coordinate2d{X: x, Y: y}, m.Shape)])
		}
		if y != m.Shape.Y-1 {
			sb.WriteRune('\n')
		}
	}
	return sb.String()
}

func NewRuneMatrixFromRows(rows []string) Matrix[rune] {
	out := NewMatrixFromShape[rune](Shape2d{X: len(rows[0]), Y: len(rows)})
	for y, row := range rows {
		for x, ch := range row {
			out.Data[RavelIndex2d(Coordinate2d{X: x, Y: y}, out.Shape)] = ch
		}
	}
	return out
}
