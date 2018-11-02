import json
import os
## Feature Requests
# Mortgage calculator (PMI, tax, HOA, insurance, equity/interest curve)
# Sweep on loan lengths
# Sweep on retirement rates
# Sweep on retirement salary
# Include separate retirement funds (account for age limits on HSA, tax changes on roth ira)
# Model paying early
# Model earnings increases
# Rent increases
# Recurring large expenses (cars, motorcycles)


recalculate = True
saved_work_filename = "plans.json"
appreciation_rate = 3.7 / 100
mortage_rate = 4.9 / 100
market_rate = 10 / 100
retirement_rate = 3 / 100
starting_amount = 9896  # Wow. Just wow. https://thecollegeinvestor.com/14611/average-net-worth-millennials/
age_death_min = 70
age_death_max = 100
current_age = 32
max_monthly_payment = 2500
house_value_min = 200000
house_value_max = 1000000
house_value_incr = 50000
down_payment_incr = 25000
retirement_salary = 45000
inflation_rate = 3.22 / 100
rent_before_purchase = 2200
loan_terms = [7, 15, 30]
social_security_age = 66

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
    # Compute how much money is needed
    total = 0
    for year in range(years):
        total = total + salary * (1+inflation_rate) ** year
    return total


def can_survive(principal, years):
    # Assume house will be bought?
    # Compute compound interest with negative contributions
    # Interest rate being (market rate - inflation)?
    # Use interest rate in retirement?
    # Is the formula similar to stock expenses?
    # This also depends on whether or not rent is being paid, assume a house will be bought?
    # Can't use compound_growth because it's been simplified to compound contributions too
    # year0 = principal - retirement_salary
    # year1 = principal + principal * (1+retirement_rate) - retirement_salary * (1+inflation_rate)
    # year3 = principal + principal * (1+retirement_rate) ** 2 - retirement_salary * (1+inflation_rate) ** 2
    required_balance = amount_needed(years, retirement_rate, retirement_salary)
    return principal < required_balance
    # balance = principal
    # for year in range(years):
    #     balance = balance * (1+retirement_rate) - retirement_salary * (1+inflation_rate) ** year
    # return balance > 0


# Retirement Age
# Death Age
# House Price
# House Down Payment
# Age of house purchase

# For all combinations of:
# death ages
    # retirement ages
        # age of purchase
            # if age < retirement_age - 15
                # down payments (increments of 25k)
                    # house values (increments of 50k)
                        # if possible and age < retirement_age_min:
                            # plan = {a, b, c, d}

plan = {}
potential_plans = []


# TODO: Rewrite without purchasing home at all
# TODO: Consider generating a matrix of options and "iterating" over that
def get_potential_plans():
    largest_simulated_down_payment = 0
    retirement_age_min = age_death_max

    for years_past_min_age_of_death in range(age_death_max - age_death_min):
        age_of_death = age_death_min + years_past_min_age_of_death
        for years_until_retirement in range(age_of_death - current_age):
            retirement_age = current_age + years_until_retirement
            for years_until_purchase in range(age_death_max - current_age):
                purchase_age = current_age + years_until_purchase
                if purchase_age > retirement_age - loan_term:
                    continue
                max_down_payment = compound_growth(starting_amount, market_rate, years_until_purchase, 12000)
                if max_down_payment > int(0.5 * house_value_max):
                    max_down_payment = int(0.5 * house_value_max)
                if largest_simulated_down_payment < max_down_payment:
                    largest_simulated_down_payment = max_down_payment

                for down_payment_multiple in range(int(max_down_payment / down_payment_incr) + 1):
                    down_payment = down_payment_multiple * down_payment_incr

                    # TODO: Factor in buying house outright and never buying (include rent in this scenario too)
                    for house_multiple in range(int((house_value_max - house_value_min) / house_value_incr) + 1):
                        house_value = house_value_min + house_multiple * house_value_incr

                        if house_value > 5 * down_payment:
                            # House incurs PMI penalty
                            continue

                        years_to_live = age_of_death - retirement_age
                        monthly_savings = max_monthly_payment - rent_before_purchase
                        balance_before_purchase = compound_growth(starting_amount,
                                                                  market_rate,
                                                                  years_until_purchase,
                                                                  12 * monthly_savings)

                        if house_value > balance_before_purchase:
                            # Cannot afford the house yet
                            continue

                        balance_after_purchase = balance_before_purchase - down_payment
                        years_from_purchase_to_retirement = retirement_age - purchase_age
                        years_from_payoff_until_retirement = retirement_age - purchase_age - loan_term

                        balance_after_appreciation = compound_growth(house_value,
                                                                appreciation_rate,
                                                                loan_term,
                                                                0)
                        balance_after_growth = compound_growth(balance_after_purchase,
                                                                                     market_rate,
                                                                                     years_from_purchase_to_retirement,
                                                                                     0)
                        balance_after_rent = compound_growth(0,
                                                             market_rate,
                                                             years_from_payoff_until_retirement,
                                                             12 * max_monthly_payment)
                        balance_at_retirement = balance_after_growth + balance_after_appreciation + balance_after_rent

                        plan = {'age_of_death': age_of_death,
                                'retirement_age': retirement_age,
                                'purchase_age': purchase_age,
                                'down_payment': down_payment,
                                'house_value': house_value,
                                'balance_at_retirement': balance_at_retirement}

                        if can_survive(balance_at_retirement, years_to_live):
                                # and retirement_age < retirement_age_min):
                            # This doesn't really find the min but does eliminate scenarios that are definitely not
                            # retirement_age_min = retirement_age
                            potential_plans.append(plan)
                            # print(f"Possible plan ${plan}")
                        # else:
                        #     print(f"Impossible ${plan}")
    return potential_plans


if os.path.isfile(saved_work_filename) and not recalculate:
    with open(saved_work_filename, 'r') as saved_work:
        potential_plans = json.loads(saved_work.read())
else:
    potential_plans = get_potential_plans()
    with open(saved_work_filename, 'w') as saved_work:
        saved_work.write(json.dumps(potential_plans))

retirement_age_min = age_death_max
highest_age_of_death = age_death_min

plans = []
# Collect min/max
for potential_plan in potential_plans:
    if potential_plan['retirement_age'] < retirement_age_min:
        retirement_age_min = potential_plan['retirement_age']
    if potential_plan['age_of_death'] > highest_age_of_death:
        highest_age_of_death = potential_plan['age_of_death']

# Produce filtered list
for potential_plan in potential_plans:
    # if potential_plan['retirement_age'] == retirement_age_min and potential_plan['age_of_death'] == highest_age_of_death:
    #     plans.append(potential_plan)
    if potential_plan['retirement_age'] == retirement_age_min:
        plans.append(potential_plan)

print(f"Earliest retirement age = {retirement_age_min}. Plans:")
for plan in plans:
    print(plan)
