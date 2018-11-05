import attr
import constants

@attr.s
class House(object):
    mortage_rate = attr.ib(default=constants.mortage_rate / 100)
    loan_term = attr.ib(default=30)
    age_at_purchase = attr.ib(default=45)
    appreciation_rate = attr.ib(default=3.7 / 100)
    down_payment = attr.ib(default=constants.down_payment_incr)
    home_value = attr.ib(default=constants.house_value_min)


@attr.s
class Plan(object):
    rate_market = attr.ib(default=7 / 100)
    rate_retirement = attr.ib(default=3 / 100)
    rate_inflation = attr.ib(default=3.22 / 100)

    age = attr.ib(default=constants.current_age)
    age_retirement = attr.ib(default=65)
    age_social_security = attr.ib(default=66)
    age_death = attr.ib(default=75)

    balance_initial = attr.ib(default=constants.starting_amount)
    max_monthly_payment = attr.ib(default=constants.max_monthly_payment)
    rent = attr.ib(default=1500)
    retirement_salary = attr.ib(default=constants.retirement_salary)


def format_currency(amount):
    return '${:,.2f}'.format(amount)


def compound_growth(principal, rate, years, annual_contribution):
    p = principal
    r = rate
    y = years
    c = annual_contribution

    if r == 0:
        r = 0.0000001

    amount = p * ((1 + r) ** y) + c * (((1 + r) ** (y + 1) - (1 + r)) / r)
    return amount


def inflation_adjusted_total(years, inflation_rate, salary):
    # print(f"Computing inflation adjusted total based on salary={salary}, years={years}, inflation rate = {inflation_rate}")
    # This is salary * geometric series using inflation rate as the variable and years as the exponent
    return salary*((1-(1+inflation_rate)**years)/(1-(1+inflation_rate)))


def simulate(plan: Plan=Plan(), house: House=None):
    # print(f"Simulating stuff with plan={plan}")

    if not house:
        # print("Running simulation without house")
        balance_at_retirement = compound_growth(plan.balance_initial,
                                                plan.rate_market,
                                                plan.age_retirement - plan.age,
                                                (plan.max_monthly_payment - plan.rent) * 12)
        # print(f"Balance at retirement {format_currency(balance_at_retirement)}")



        # Next two amounts are computed to account for inflation while still working
        # Most models assume a sensible retirement salary by today's standards
        # At best, they begin inflating the salary at retirement (that's 20-30 years of ignored growth!)
        amount_needed_until_death = inflation_adjusted_total(plan.age_death - plan.age,
                                                  plan.rate_inflation,
                                                  plan.retirement_salary)
        # print(f"Amount needed until death {format_currency(amount_needed_until_death)}")

        # If this method were still iterative, I would call from age to retirement and from retirement to death
        # ... but it's not ... not anymore =)
        amount_needed_until_retire = inflation_adjusted_total(plan.age_retirement - plan.age,
                                                  plan.rate_inflation,
                                                  plan.retirement_salary)
        # print(f"Amount needed until retirement age {format_currency(amount_needed_until_retire)}")

        amount_needed_for_retirement = amount_needed_until_death - amount_needed_until_retire
        # print(f"Amount needed to live {format_currency(amount_needed_for_retirement)}")

        avg_sal_per_year = amount_needed_for_retirement / (plan.age_death - plan.age_retirement)
        # print(f"Average salary during retirement {format_currency(avg_sal_per_year)}")

        amount_leftover = balance_at_retirement - amount_needed_for_retirement
        # print(f"Amount leftover {format_currency(amount_leftover)}")

        return amount_leftover


print("Simulating default plan")
default = Plan()
simulate()

print("Generating other plans")
plans = []
for age_retirement in range(default.age, 65):
    for salary_retirement in range(30000, 60000, 5000):
        for age_death in range(75, 115):
            plans.append(Plan(age_retirement=age_retirement, retirement_salary=salary_retirement, age_death=age_death))

print(f"Generated {len(plans)} options.")

successful_plans = {}
for i, plan in enumerate(plans):
    balance = simulate(plan)
    if balance > 0:
        # print("Simulated plan number " + str(i + 1) + " was a success!")
        successful_plans[i] = {'plan': plan, 'balance': balance}
    # else:
        # print("Simulated plan number " + str(i + 1) + " was a failure.")

print(f"Found {len(successful_plans)} successful plans!")

oldest_death = 0
oldest_death_ids = []
earliest_retirement = 115
earliest_retirement_ids = []
largest_balance = 0
largest_balance_ids = []

for plan_id, successful_plan in successful_plans.items():
    if successful_plan['plan'].age_death > oldest_death:
        oldest_death = successful_plan['plan'].age_death
    if successful_plan['plan'].age_retirement < earliest_retirement:
        earliest_retirement = successful_plan['plan'].age_retirement
    if successful_plan['balance'] > largest_balance:
        largest_balance = successful_plan['balance']

for plan_id, successful_plan in successful_plans.items():
    if successful_plan['plan'].age_death == oldest_death:
        oldest_death_ids.append(plan_id)
    if successful_plan['plan'].age_retirement == earliest_retirement:
        earliest_retirement_ids.append(plan_id)
    if successful_plan['balance'] == largest_balance:
        largest_balance_ids.append(plan_id)

print(f"Oldest Death = {oldest_death}, found {len(oldest_death_ids)} plans")
print(f"Earliest Retirement = {earliest_retirement}, found {len(earliest_retirement_ids)} plans")
print(f"Largest Balance = {largest_balance}, found {len(largest_balance_ids)} plans")
print(f"Earliest retirement plan: {successful_plans[earliest_retirement_ids[0]]}")

earliest_retirement = 115
earliest_retirement_id = -1
for oldest_death_id in oldest_death_ids:
    plan = successful_plans[oldest_death_id]['plan']
    if plan.age_retirement < earliest_retirement:
        earliest_retirement = plan.age_retirement
        earliest_retirement_id = oldest_death_id

print(f"Earliest retirement for oldest death is {successful_plans[earliest_retirement_id]}")
print(f"Plan with largest balance is {successful_plans[largest_balance_ids[0]]}")