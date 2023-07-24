

# https://www.codewars.com/kata/566584e3309db1b17d000027


import re


def differentiate(equation, point):
    derivative = ""
    for operator, factor, exponent in re.findall(r"(?:([+-]))?([0-9]*)x(?:\^([0-9]+))?", equation):
        factor = factor or "1"
        exponent = exponent or "1"
        derivative += f"{operator}{factor}*{exponent}*({point})**({exponent}-1)"

    return eval(derivative)

print(differentiate("12x+2", 3))  # , 12
print(differentiate("x^2-x", 3))  # , 5
print(differentiate("-5x^2+10x+4", 3))  # , -20
