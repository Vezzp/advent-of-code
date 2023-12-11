package jogtrot

import (
	"bufio"
	"cmp"
	"flag"
	"fmt"
	"os"

	"golang.org/x/exp/constraints"
)

type Number interface {
	int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64 | uintptr | float32 | float64
}

func ReadFileRows(filepath string) []string {
	var rows []string
	file, err := os.Open(filepath)
	defer func() {
		if err := file.Close(); err != nil {
			panic(err)
		}
	}()

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		rows = append(rows, scanner.Text())
	}

	if len(rows) == 0 {
		panic(fmt.Sprintf("File %s is empty", filepath))
	}

	return rows
}

func LoWrapIndex[P, R any](fn func(P) R) func(P, int) R {
	return func(item P, _ int) R {
		return fn(item)
	}
}

func PrintSolution(part int, solution any) {
	fmt.Printf("Part %d solution: %v\n", part, solution)
}

func SliceMap[T, R any](slice []T, fn func(T) R) []R {
	out := make([]R, len(slice))
	for idx, item := range slice {
		out[idx] = fn(item)
	}
	return out
}

func SliceMapWithIndex[T, R any](slice []T, fn func(T, int) R) []R {
	out := make([]R, len(slice))
	for idx, item := range slice {
		out[idx] = fn(item, idx)
	}
	return out
}

func SliceIntersection[T cmp.Ordered](lhs, rhs []T) []T {
	var out []T
	visited := make(map[T]bool)
	for _, item := range lhs {
		visited[item] = true
	}
	for _, item := range rhs {
		if _, ok := visited[item]; ok {
			out = append(out, item)
		}
	}
	return out
}

func SliceEveryBy[T any](lst []T, fn func(T) bool) bool {
	for _, item := range lst {
		if !fn(item) {
			return false
		}
	}
	return true
}

func SliceFilter[T any](lst []T, fn func(T) bool) []T {
	out := make([]T, 0, len(lst)/2)
	for _, item := range lst {
		if fn(item) {
			out = append(out, item)
		}
	}
	return out
}

func SliceSum[T Number](lst []T) T {
	out := T(0)
	for _, item := range lst {
		out += item
	}
	return out
}

func SliceSumBy[T any, R Number](lst []T, fn func(T) R) R {
	out := R(0)
	for _, item := range lst {
		out += fn(item)
	}
	return out
}

func SliceFlatten[T any](lst [][]T) []T {
	out := make([]T, 0, len(lst))
	for _, item := range lst {
		out = append(out, item...)
	}
	return out
}

func SliceAll[T cmp.Ordered](lst []T, fn func(T) bool) bool {
	for _, item := range lst {
		if !fn(item) {
			return false
		}
	}
	return true
}

func GCD[T constraints.Integer](a, b T) T {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func LCM[T constraints.Integer](a, b T) T {
	return (a * b) / GCD(a, b)
}

func SliceReduce[T any](lst []T, fn func(T, T) T) T {
	out := lst[0]
	for _, item := range lst[1:] {
		out = fn(out, item)
	}
	return out
}

func SliceFirst[T any](lst []T) T {
	return lst[0]
}

func SliceLast[T any](lst []T) T {
	return lst[len(lst)-1]
}

func NewDefaultSlice[T any](n int, v T) []T {
	out := make([]T, 0, n)
	for i := 0; i < n; i++ {
		out = append(out, v)
	}
	return out
}

func ParseCommandLine() ([]string, string) {
	var part, input string

	flag.StringVar(&part, "p", "", "Puzzle part to solve")
	flag.StringVar(&input, "i", "./input.txt", "File with puzzle input")
	flag.Parse()

	if _, err := os.Stat(input); err != nil {
		panic(err)
	}

	parts := make([]string, 0)
	switch part {
	case "1", "2":
		parts = append(parts, part)
	default:
		parts = append(parts, "1", "2")
	}

	return parts, input
}

func Abs[T constraints.Integer | constraints.Float](n T) T {
	if n < 0 {
		return -n
	}
	return n
}

func ManhattanDistance2d(lhs, rhs Coordinate2d) int {
	return Abs(lhs.X-rhs.X) + Abs(lhs.Y-rhs.Y)
}

func MinMax[T Number](n T, ns ...T) (T, T) {
	min_ := n
	max_ := n
	for _, item := range ns {
		min_ = min(min_, item)
		max_ = max(max_, item)
	}
	return min_, max_
}
