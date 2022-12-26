from __future__ import annotations

from collections import deque

SNAFU_BASE = 5


SNAFU_DIGIT_TO_DECIMAL = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

BALANCED_DIGIT_TO_SNAFU = {
    3: "=",
    4: "-",
    5: "0",
}


def convert_snafu_to_decimal(snafu: str, /) -> int:
    out = 0
    for idx, digit in enumerate(reversed(snafu)):
        out += SNAFU_DIGIT_TO_DECIMAL[digit] * SNAFU_BASE**idx

    return out


def convert_decimal_to_snafu(decimal: int, /) -> str:
    remainders = deque()
    while (leftover := decimal // SNAFU_BASE) >= SNAFU_BASE:
        remainder = decimal % SNAFU_BASE
        remainders.append(remainder)
        decimal = leftover
    remainders.append(decimal % SNAFU_BASE)
    remainders.append(leftover)

    digits = []
    while len(remainders) != 0:
        match (remainder := remainders.popleft()):
            case 0 | 1 | 2:
                digit = str(remainder)

            case 3 | 4 | 5:
                digit = BALANCED_DIGIT_TO_SNAFU[remainder]
                if len(remainders) == 0:
                    remainders.append(1)
                else:
                    remainders[0] += 1

            case _:
                raise ValueError(remainder)

        digits.append(digit)

    out = "".join(reversed(digits))

    return out
