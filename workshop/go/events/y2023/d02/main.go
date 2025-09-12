package main

import (
	"fmt"
	"strings"

	"aoc/elf"
)

type Game struct {
	ID     int
	Rounds []Round
}

func (g *Game) IsRoundConfigrationValid(c Configuration) bool {
	return elf.SliceEveryBy(
		g.Rounds,
		func(r Round) bool {
			return r.R <= c.R && r.G <= c.G && r.B <= c.B
		},
	)
}

func (g *Game) MinConfiguration() Configuration {
	if len(g.Rounds) == 0 {
		return Configuration{}
	}
	var c Configuration
	{
		r := g.Rounds[0]
		c.R = r.R
		c.G = r.G
		c.B = r.B
	}

	for _, r := range g.Rounds {
		c.R = max(c.R, r.R)
		c.G = max(c.G, r.G)
		c.B = max(c.B, r.B)
	}

	return c
}

type RGB struct {
	R int
	G int
	B int
}

type (
	Round         RGB
	Configuration RGB
)

func (c *Configuration) Power() int64 {
	return int64(c.R) * int64(c.G) * int64(c.B)
}

func ParseGameFromStr(str string) Game {
	var ID int
	prefixFmt := "Game %d: "
	if _, err := fmt.Sscanf(str, prefixFmt, &ID); err != nil {
		panic(fmt.Sprintf("Cannot parse game from line '%s'", str))
	}

	rawRounds := strings.Split(strings.TrimPrefix(str, fmt.Sprintf(prefixFmt, ID)), ";")
	rounds := elf.SliceMap(rawRounds, ParseRoundFromStr)

	return Game{ID: ID, Rounds: rounds}
}

func ParseRoundFromStr(str string) Round {
	round := Round{}
	rawRGBSets := strings.Split(str, ",")

	var count int
	var RGB string
	for _, rawRGBSet := range rawRGBSets {
		if _, err := fmt.Sscanf(rawRGBSet, "%d %s", &count, &RGB); err != nil {
			panic(fmt.Sprintf("Cannot parse RGB set from line %s", str))
		}

		switch RGB {
		case "red":
			round.R = count
		case "green":
			round.G = count
		case "blue":
			round.B = count
		default:
			panic(fmt.Sprintf("Unknown RGB %s", RGB))
		}
	}

	return round
}

func SolveFirstPart(filepath string) {
	target := Configuration{R: 12, G: 13, B: 14}
	rows := elf.ReadFileRows(filepath)

	solution := elf.SliceSumBy(
		elf.SliceFilter(
			elf.SliceMap(rows, ParseGameFromStr),
			func(g Game) bool {
				return g.IsRoundConfigrationValid(target)
			},
		),
		func(g Game) int { return g.ID },
	)

	elf.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := elf.ReadFileRows(filepath)
	games := elf.SliceMap(rows, ParseGameFromStr)

	solution := int64(0)
	for _, g := range games {
		c := g.MinConfiguration()
		solution += c.Power()
	}

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
