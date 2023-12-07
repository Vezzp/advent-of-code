package jogtrot

import (
	"bufio"
	"cmp"
	"fmt"
	"os"
)

func ReadFileRows(filepath string) ([]string, error) {
	var rows []string
	file, err := os.Open(filepath)
	defer func() {
		if err := file.Close(); err != nil {
			panic(err)
		}
	}()

	if err != nil {
		return rows, err
	}

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		rows = append(rows, scanner.Text())
	}

	return rows, nil
}

func LoWrapIndex[P, R any](fn func(P) R) func(P, int) R {
	return func(item P, _ int) R {
		return fn(item)
	}
}

func PrintFirstPartSolution(s any) {
	fmt.Printf("The first part solution is: %v\n", s)
}

func PrintSecondPartSolution(s any) {
	fmt.Printf("The second part solution is: %v\n", s)
}

func SliceMap[T, R any](slice []T, fn func(T) R) []R {
	out := make([]R, len(slice))
	for idx, item := range slice {
		out[idx] = fn(item)
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
