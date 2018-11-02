from money import compound_growth
from constants import current_age, starting_amount, market_rate, max_monthly_payment, rent_before_purchase
from json import JSONEncoder, JSONDecoder


class ScenarioEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def as_scenario(dct):
    return Scenario(dct['death_age'], dct['retirement_age'], dct['purchase_age'], dct['down_payment'],
             dct['house_value'], dct['loan_term'], dct['savings_at_purchase'])


# TODO: Subclass for different types of scenarios
class Scenario:

    def __init__(self, death_age,
                 retirement_age,
                 purchase_age,
                 down_payment,
                 house_value,
                 loan_term,
                 savings_at_purchase=0):
        self.death_age = death_age
        self.retirement_age = retirement_age
        self.purchase_age = purchase_age
        self.down_payment = down_payment
        self.house_value = house_value
        self.loan_term = loan_term
        self.savings_at_purchase = savings_at_purchase

    def amount_saved(self):  # TODO: Consider caching values
        monthly_savings = max_monthly_payment - rent_before_purchase
        annual_contribution = 12 * monthly_savings
        years_to_save = self.purchase_age - current_age
        self.savings_at_purchase = compound_growth(starting_amount, market_rate, years_to_save, annual_contribution)
        return self.savings_at_purchase

    def is_valid(self):
        # TODO: Account for survival
        # TODO: Put class-specific validation in separate classes (down payment validation, $0 rent calculations, etc.)
        return (self.purchase_age < self.retirement_age - self.loan_term and
                self.retirement_age < self.death_age and
                self.house_value > self.down_payment >= self.house_value / 5 and
                self.down_payment < self.amount_saved())

    def __str__(self):
        return (f"Scenario[ "
                f"retirement age = {self.retirement_age}, "
                f"purchase age = {self.purchase_age} "
                f"down payment = {self.down_payment} "
                f"house_value = {self.house_value} "
                f"loan_term = {self.loan_term} "
                f"savings at purchase = {self.savings_at_purchase}"
                f"]")
