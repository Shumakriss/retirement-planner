def simulate(info):

    ages = [x + info.age for x in range(info.age_death - info.age + 1)]
    years = [info.current_year]
    balances = []

    # TODO: Make home purchase and social security optional
    # TODO: Factor in taxes based on account type
    # TODO: Think through contribution/compounding periods and adjust accordingly
    # TODO: Plot against time: retirement salary, home value, equity, interest paid, rent rate inflation
    for age in ages:
        years.append(years[-1] + 1)
        salary_retirement = salary_retirement * (1 + info.rate_inflation)
        if age == info.age_purchase:
            if info.purchase_type == "mortgage":
                savings_retirement = savings_retirement - info.down_payment
            elif info.purchase_type == "outright":
                savings_retirement = savings_retirement - house_value
        if age > info.age_purchase:
            house_value = house_value * (1 + info.rate_appreciation)
        if info.age_retirement > age > info.age_purchase + info.loan_term:
            savings_retirement = savings_retirement + 12 * info.rent
        if age < info.age_retirement:
            savings_retirement = savings_retirement * (1.0 + info.market_rate)    # TODO: Why is this a string?
            savings_retirement = savings_retirement + 12 * info.contribution_monthly
        else:
            savings_retirement = savings_retirement * (1 + info.rate_retirement)
            savings_retirement = savings_retirement - salary_retirement
        if age > info.age_social_security:
            savings_retirement = savings_retirement + 12 * info.monthly_contribution_social_security
        if savings_retirement < 0:
            savings_retirement = 0
        balances.append(savings_retirement)

    return ages, balances
