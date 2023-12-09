package jogtrot

import (
	"bufio"
	"cmp"
	"fmt"
	"os"

	"golang.org/x/exp/constraints"
)

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

func SliceSum[T constraints.Float | constraints.Integer](lst []T) T {
	out := T(0)
	for _, item := range lst {
		out += item
	}
	return out
}

func SliceSumBy[T any, R constraints.Float | constraints.Integer](lst []T, fn func(T) R) R {
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
