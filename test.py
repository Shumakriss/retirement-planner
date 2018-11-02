from constants import appreciation_rate
from constants import mortage_rate
from constants import market_rate
from constants import retirement_rate
from constants import starting_amount
from constants import age_death_min
from constants import age_death_max
from constants import current_age
from constants import loan_terms
from constants import max_monthly_payment
from constants import house_value_min
from constants import house_value_max
from constants import house_value_incr
from constants import down_payment_incr
from constants import retirement_salary
from constants import inflation_rate
from constants import rent_before_purchase
from constants import social_security_age

from scenarios import Scenario, ScenarioEncoder, as_scenario

import json
import os

## Feature Reqeusts
# Don't sweep, create a GUI, allow plotting multiple scenarios simultaneously
# Once all of the modeling options are understood/integrated, then sweep or optimize
# TODO: Wrap this as a "simulation" and subclass it?

down_payment_scenarios_filename = "down_payment_scenarios.json"
valid_down_payment_scenarios_filename = "valid_down_payment_scenarios.json"
recalculate_down_payment_scenarios = False
recalculate_valid_down_payment_scenarios = False

# Generate all scenarios
death_ages = list(range(age_death_min, age_death_max+1))
retirement_ages = list(range(current_age, social_security_age+1))
purchase_ages = list(range(current_age, social_security_age-min(loan_terms)+1))

down_payments = []
for down_payment in range(down_payment_incr, house_value_max, down_payment_incr):
    down_payments.append(down_payment)

house_values = []
for house_value in range(house_value_min, house_value_max, house_value_incr):
    house_values.append(house_value)


def get_down_payment_scenarios():
    count = 0
    down_payment_scenarios = []
    for death_age in death_ages:
        for retirement_age in retirement_ages:
            for purchase_age in purchase_ages:
                for down_payment in down_payments:
                    for house_value in house_values:
                        for loan_term in loan_terms:
                            scenario = Scenario(death_age,
                                                retirement_age,
                                                purchase_age,
                                                down_payment,
                                                house_value,
                                                loan_term)
                            down_payment_scenarios.append(scenario)
                            count = count + 1
                            if count > 500000:
                                return down_payment_scenarios
                            if count % 500000 == 0:
                                print(f"{count}: {scenario}")
    return down_payment_scenarios


down_payment_scenarios = []
if os.path.isfile(down_payment_scenarios_filename) and not recalculate_down_payment_scenarios:
    print("Found down payment scenarios")
    with open(down_payment_scenarios_filename, 'r') as scenarios_file:
        down_payment_scenarios = json.loads(scenarios_file.read(), object_hook=as_scenario)
    print("Loaded down payment scenarios")
else:
    print("Did not find down payment scenarios or forced to recalculate")
    count = len(death_ages) * len(retirement_ages) * len(purchase_ages) * \
            len(down_payments) * len(house_values) * len(loan_terms)
    print(f"Expecting {count} down payment scenarios")
    down_payment_scenarios = get_down_payment_scenarios()
    with open(down_payment_scenarios_filename, 'w') as scenarios_file:
        scenarios_file.write(json.dumps(down_payment_scenarios, cls=ScenarioEncoder))
    print("Wrote down payment scenarios")


def get_valid_scenarios(scenarios):
    valid_scenarios = []
    for scenario in scenarios:
        if scenario.is_valid():
            valid_scenarios.append(scenario)
    return valid_scenarios


valid_down_payment_scenarios = []
if os.path.isfile(valid_down_payment_scenarios_filename) and not recalculate_valid_down_payment_scenarios:
    print("Found valid down payment scenarios")
    with open(valid_down_payment_scenarios_filename, 'r') as scenarios_file:
        scenarios = json.loads(scenarios_file.read(), object_hook=as_scenario)
    print("Loaded valid down payment scenarios")
else:
    print("Did not find valid down payment scenarios or forced to recalculate")
    scenarios = get_valid_scenarios(down_payment_scenarios)
    with open(valid_down_payment_scenarios_filename, 'w') as scenarios_file:
        scenarios_file.write(json.dumps(scenarios, cls=ScenarioEncoder))
    print("Wrote valid down payment scenarios")
