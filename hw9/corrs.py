import math


def parse_table(t: list[list[float]]) -> dict[str, float]:
    height, width = len(t) - 1, len(t[0]) - 1

    prob_x = [sum(t[y + 1][x + 1] for y in range(height)) for x in range(width)]
    prob_y = [sum(t[y + 1][x + 1] for x in range(width)) for y in range(height)]

    values_x = [t[0][x + 1] for x in range(width)]
    values_y = [t[y + 1][0] for y in range(height)]

    exp_x = calc_exp(values_x, prob_x)
    exp_y = calc_exp(values_y, prob_y)

    disp_x = calc_disp(values_x, prob_x)
    disp_y = calc_disp(values_y, prob_y)

    prob_xy = [t[y + 1][x + 1] for x in range(width) for y in range(height)]
    values_xy = [values_x[x] * values_y[y] for x in range(width) for y in range(height)]
    exp_xy = calc_exp(values_xy, prob_xy)

    cov = exp_xy - exp_x * exp_y
    corr = cov / math.sqrt(disp_x * disp_y)

    return {
        "exp_x": exp_x,
        "exp_y": exp_y,
        "exp_xy": exp_xy,
        "disp_x": disp_x,
        "disp_y": disp_y,
        "cov": cov,
        "corr": corr,
    }


def calc_exp(values: list[float], prob: list[float]) -> float:
    return sum(values[i] * prob[i] for i in range(len(values)))


def calc_disp(values: list[float], prob: list[float]) -> float:
    return calc_exp([v * v for v in values], prob) - calc_exp(values, prob) ** 2


def parse_float(s: str) -> float:
    parts = s.split("/")
    if len(parts) > 2:
        raise ValueError(f"invalid value: {s}")
    if len(parts) == 2:
        return float(parts[0]) / float(parts[1])
    return float(parts[0])


if __name__ == "__main__":
    print("Enter table in format")
    print("0       x-val1  x-val2  ...  x-valN")
    print("y-val1  prob11  prob21  ...  probN1")
    print("y-val2  prob12  prob22  ...  probN2")
    print("...     ...     ...     ...  ...")
    print("y-valN  prob1N  prob2N  ...  probNN")
    print("END")
    print("you can also use fractional values like 1/3")
    print()

    table = []
    while True:
        line = input()
        if line == "END":
            break
        table.append([parse_float(x) for x in line.split()])

    result = parse_table(table)
    for k, v in result.items():
        print(f"{k}: {v}")
