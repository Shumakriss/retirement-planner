def compound_growth(principal, rate, years, annual_contribution):
    p = principal
    r = rate
    y = years
    c = annual_contribution

    if r == 0:
        r = 0.0000001

    amount = p * ((1 + r) ** y) + c * (((1 + r) ** (y + 1) - (1 + r)) / r)
    return amount


def print_currency(currency):
    print('${:,.2f}'.format(currency))


def amount_needed(years, inflation_rate, salary):
    total = 0
    for year in range(years):
        total = total + salary * (1+inflation_rate) ** year
    return total


def can_survive(principal, years, retirement_rate, retirement_salary):
    required_balance = amount_needed(years, retirement_rate, retirement_salary)
    return principal < required_balance
