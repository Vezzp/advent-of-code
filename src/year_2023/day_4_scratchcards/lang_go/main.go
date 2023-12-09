package main

import (
	"fmt"
	"strconv"
	"strings"

	"advent_of_code/jogtrot"
)

type Card struct {
	ID             int
	WinningNumbers []int
	PlayingNumbers []int
}

func (c *Card) MatchingNumbers() []int {
	return jogtrot.SliceIntersection(c.WinningNumbers, c.PlayingNumbers)
}

func (c *Card) Points() int {
	out := 0
	switch num := len(c.MatchingNumbers()); num {
	case 0:
	default:
		out += (1 << (num - 1))
	}
	return out
}

func ParseCardFromStr(str string) Card {
	rawID, rawNumbers, _ := strings.Cut(
		strings.TrimSpace(strings.TrimPrefix(str, "Card")),
		":",
	)

	ID, err := strconv.Atoi(strings.TrimSpace(rawID))
	if err != nil {
		panic(fmt.Sprintf("Cannot parse card ID from line '%s'", str))
	}

	rawWinningNumbers, rawPlayingNumbers, _ := strings.Cut(strings.TrimSpace(rawNumbers), "|")

	return Card{
		ID:             ID,
		WinningNumbers: ParseNumbersFromStr(rawWinningNumbers),
		PlayingNumbers: ParseNumbersFromStr(rawPlayingNumbers),
	}
}

func ParseNumbersFromStr(str string) []int {
	var out []int
	for _, el := range strings.Fields(strings.TrimSpace(str)) {
		number, err := strconv.Atoi(el)
		if err != nil {
			panic(err)
		}
		out = append(out, number)
	}
	return out
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	cards := jogtrot.SliceMap(rows, ParseCardFromStr)

	solution := 0
	for _, card := range cards {
		solution += card.Points()
	}

	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	cards := jogtrot.SliceMap(rows, ParseCardFromStr)
	cardIDToCount := make(map[int]int64)
	for _, card := range cards {
		cardIDToCount[card.ID] += 1
		numCopies := cardIDToCount[card.ID]

		for i := 1; i <= len(card.MatchingNumbers()); i++ {
			cardIDToCount[card.ID+i] += numCopies
		}
	}

	solution := int64(0)
	for _, val := range cardIDToCount {
		solution += val
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
