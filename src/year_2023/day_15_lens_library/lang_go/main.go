package main

import (
	"fmt"
	"strconv"
	"strings"
	"unicode"

	"advent_of_code/jogtrot"
)

type Operation rune

const (
	OperationDash      Operation = '-'
	OperationEqualSign Operation = '='
)

func LabelHash(s string) int {
	out := int64(0)
	for _, s := range s {
		out += int64(s)
		out *= 17
		out %= 256
	}
	return int(out)
}

type Lens struct {
	Label       string
	FocalLength int
}

func (l Lens) String() string {
	return fmt.Sprintf("[%s %d]", l.Label, l.FocalLength)
}

type Box []Lens

func (b *Box) Emplace(label string, focalLength int) {
	if idx := jogtrot.SliceFindFirstBy(*b, func(l Lens) bool { return l.Label == label }); idx == -1 {
		(*b) = append((*b), Lens{label, focalLength})
	} else {
		(*b)[idx].FocalLength = focalLength
	}
}

func (b *Box) Remove(label string) {
	if idx := jogtrot.SliceFindFirstBy(*b, func(l Lens) bool { return l.Label == label }); idx != -1 {
		(*b) = jogtrot.SliceRemoveIndex(*b, idx)
	}
}

type Bucket []Box

func (b Bucket) String() string {
	var sb strings.Builder
	for idx, lenses := range b {
		if len(lenses) == 0 {
			continue
		}
		if idx != 0 {
			sb.WriteRune('\n')
		}
		sb.WriteString(fmt.Sprintf("Box %d: ", idx))

		for idx, lens := range lenses {
			if idx != 0 {
				sb.WriteRune(' ')
			}
			sb.WriteString(lens.String())
		}
	}
	return sb.String()
}

func (b Bucket) Operate(step string) {
	var (
		label       string
		focalLength int
		operation   Operation
		err         error
	)
	if unicode.IsDigit(rune(step[len(step)-1])) {
		operation = OperationEqualSign
		parts := strings.Split(step, string(operation))
		label = parts[0]

		focalLength, err = strconv.Atoi(parts[1])
		if err != nil {
			panic(err)
		}

	} else {
		operation = OperationDash
		label = strings.TrimSuffix(step, string(OperationDash))
	}

	labelHash := LabelHash(label)

	box := b[labelHash]
	switch operation {
	case OperationDash:
		box.Remove(label)
	case OperationEqualSign:
		box.Emplace(label, focalLength)
	}
	b[labelHash] = box
}

func SolveFirstPart(filepath string) {
	row := jogtrot.ReadFileRows(filepath)[0]
	solution := 0
	for _, step := range strings.Split(row, ",") {
		solution += LabelHash(step)
	}
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	row := jogtrot.ReadFileRows(filepath)[0]
	bucket := Bucket(make([]Box, 256))
	for _, step := range strings.Split(row, ",") {
		bucket.Operate(step)
	}
	solution := 0
	for boxIdx, lenses := range bucket {
		for slotIdx, lens := range lenses {
			solution += (boxIdx + 1) * (slotIdx + 1) * lens.FocalLength
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
