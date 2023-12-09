package main

import (
	"fmt"
	"strconv"
	"strings"
	"unicode"

	"advent_of_code/jogtrot"
)

var SpellToDigit = map[string]string{
	"one":   "1",
	"two":   "2",
	"three": "3",
	"four":  "4",
	"five":  "5",
	"six":   "6",
	"seven": "7",
	"eight": "8",
	"nine":  "9",
}

func ReplaceSpelledDigits(str string) string {
	builder := strings.Builder{}

charLoop:
	for idx, char := range str {
		for spell, digit := range SpellToDigit {
			if strings.HasPrefix(str[idx:], spell) {
				builder.WriteString(digit)
				continue charLoop
			}
		}
		builder.WriteRune(char)
	}

	return builder.String()
}

func Solve(rows []string) int {
	out := 0
	for _, row := range rows {
		var digits []rune
		for _, char := range row {
			if unicode.IsDigit(char) {
				digits = append(digits, char)
			}
		}
		if number, err := strconv.Atoi(fmt.Sprintf("%c%c", digits[0], jogtrot.SliceLast(digits))); err == nil {
			out += number
		}
	}
	return out
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	solution := Solve(rows)
	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	rows = jogtrot.SliceMap(rows, ReplaceSpelledDigits)
	solution := Solve(rows)
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
