package main

import (
	"flag"
	"fmt"
	"os"
	"sort"

	"advent_of_code/jogtrot"
)

type Card uint8

func NewCardFromRune(r rune) Card {
	switch r {
	case '2':
		return Deuce
	case '3':
		return Three
	case '4':
		return Four
	case '5':
		return Five
	case '6':
		return Six
	case '7':
		return Seven
	case '8':
		return Eight
	case '9':
		return Nine
	case 'T':
		return Ten
	case 'J':
		return Jack
	case 'Q':
		return Queen
	case 'K':
		return King
	case 'A':
		return Ace
	case 'W':
		return Joker
	default:
		panic(fmt.Sprintf("Unexpected card: %c", r))
	}
}

const (
	Joker Card = iota
	Deuce
	Three
	Four
	Five
	Six
	Seven
	Eight
	Nine
	Ten
	Jack
	Queen
	King
	Ace
)

type HandStrength uint8

const (
	HighCard HandStrength = iota + 1
	OnePair
	TwoPairs
	ThreeOfAKind
	FullHouse
	FourOfAKind
	FiveOfAKind
)

type Hand [5]Card

func (h *Hand) ReplaceMap(m map[Card]Card) {
	for idx, card := range *h {
		if newCard, ok := m[card]; ok {
			(*h)[idx] = newCard
		}
	}
}

func (h Hand) Strength() HandStrength {
	cardToCount := make(map[Card]int)
	for _, r := range h {
		cardToCount[r] += 1
	}

	type CardCount struct {
		Card  Card
		Count int
	}

	jokerCount, jokerOK := cardToCount[Joker]
	if jokerOK {
		delete(cardToCount, Joker)
	}

	cardCounts := make([]CardCount, 0)
	for card, count := range cardToCount {
		cardCounts = append(
			cardCounts,
			CardCount{
				Card:  card,
				Count: count,
			},
		)
	}
	sort.Slice(
		cardCounts,
		func(lidx, ridx int) bool {
			return cardCounts[lidx].Count > cardCounts[ridx].Count
		},
	)

	if jokerOK {
		if len(cardCounts) == 0 {
			cardCounts = append(cardCounts, CardCount{Card: Ace, Count: jokerCount})
		} else {
			cardCounts[0].Count += jokerCount
		}
	}

	switch num := len(cardCounts); num {
	case 1:
		return FiveOfAKind
	case 2, 3:
		switch cardCounts[0].Count {
		case 4:
			return FourOfAKind
		case 3:
			if cardCounts[1].Count == 2 {
				return FullHouse
			}
			return ThreeOfAKind
		case 2:
			return TwoPairs
		default:
			panic(fmt.Sprintf("Unexpected hand combination: %v", h))
		}
	case 4:
		return OnePair
	case 5:
		return HighCard
	default:
		panic(fmt.Sprintf("Unexpected hand combination: %v", h))
	}
}

func HandLessComparator(lhs, rhs Hand) bool {
	lhsStrength := lhs.Strength()
	rhsStrength := rhs.Strength()
	if lhsStrength != rhsStrength {
		return lhsStrength < rhsStrength
	}
	for i := 0; i < 5; i++ {
		if lhs[i] != rhs[i] {
			return lhs[i] < rhs[i]
		}
	}
	return true
}

type CamelBid struct {
	Hand Hand
	Bid  int
}

func ParseCamelBidFromStr(str string) CamelBid {
	var bid int
	var rawHand string

	fmt.Sscanf(str, "%s %d", &rawHand, &bid)

	return CamelBid{
		Hand: ParseHandFromStr(rawHand),
		Bid:  bid,
	}
}

func ParseHandFromStr(str string) Hand {
	if len(str) != 5 {
		panic(fmt.Sprintf("Unexpected hand length: %s", str))
	}
	var hand Hand
	for i, r := range str {
		hand[i] = NewCardFromRune(r)
	}
	return hand
}

func SolveFirstPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	camelBids := jogtrot.SliceMap(rows, ParseCamelBidFromStr)
	sort.Slice(
		camelBids,
		func(lidx, ridx int) bool {
			return HandLessComparator(camelBids[lidx].Hand, camelBids[ridx].Hand)
		},
	)

	solution := int64(0)
	for idx, camelBid := range camelBids {
		solution += int64(idx+1) * int64(camelBid.Bid)
	}

	jogtrot.PrintSolution(1, solution)
}

func SolveSecondPart(filepath string) {
	rows := jogtrot.ReadFileRows(filepath)
	camelBids := jogtrot.SliceMap(rows, ParseCamelBidFromStr)
	for idx := 0; idx < len(camelBids); idx++ {
		camelBids[idx].Hand.ReplaceMap(map[Card]Card{Jack: Joker})
	}

	sort.Slice(
		camelBids,
		func(lidx, ridx int) bool {
			return HandLessComparator(camelBids[lidx].Hand, camelBids[ridx].Hand)
		},
	)

	solution := int64(0)
	for idx, camelBid := range camelBids {
		solution += int64(idx+1) * int64(camelBid.Bid)
	}

	jogtrot.PrintSolution(2, solution)
}

func main() {
	var part string

	flag.StringVar(&part, "p", "Part to solve", "Part to solve")
	flag.Parse()

	parts := make([]string, 0)
	switch part {
	case "1", "2":
		parts = append(parts, part)
	default:
		parts = append(parts, "1", "2")
	}

	var src string
	args := flag.Args()
	switch len(args) {
	case 0:
		src = "./input.txt"
		if _, err := os.Stat(src); err != nil {
			panic("When no puzzle input is given, ./input.txt must exist")
		}

	case 1:
		src = args[0]
	default:
		panic(fmt.Sprintf("Solver accepts no or single puzzle files, got %d", len(args)))
	}

	for _, part := range parts {
		switch part {
		case "1":
			SolveFirstPart(src)
		case "2":
			SolveSecondPart(src)
		}
	}
}
