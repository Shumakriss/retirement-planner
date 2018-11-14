import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# TODO: Is there an off by one error? The graph doesn't peak at age_retirement but age_retirement-1

now = datetime.datetime.now()
current_year = now.year
defaults = {
    'age_retirement': 65,
    'age': 32,
    'age_death': 80,
    'savings_retirement': 10000,
    'market_rate': (7 / 100),
    'rate_retirement': (3 / 100),
    'rate_appreciation': (3.7 / 100),
    'rate_inflation': (3.22 / 100),
    # 'rate_contribution': (5 / 100),
    'contribution_monthly': 200,
    'rent': 1500,
    'salary_retirement': 20000,
    'down_payment': 14000,
    'house_value': 250000,
    'loan_term': 30,
    'age_purchase': 35,
    'purchase_type': "mortgage",
    'age_social_security': 65,
    'monthly_contribution_social_security': 3698,
    # 'house': True,
    # 'social_security': True
}


def recalculate(age_retirement=defaults['age_retirement'],
                age=defaults['age'],
                age_death=defaults['age_death'],
                savings_retirement=defaults['savings_retirement'],
                market_rate=defaults['market_rate'],
                rate_retirement=defaults['rate_retirement'],
                rate_appreciation=defaults['rate_appreciation'],
                rate_inflation=defaults['rate_inflation'],
                # rate_contribution=defaults['rate_contribution'],
                contribution_monthly=defaults['contribution_monthly'],
                rent=defaults['rent'],
                salary_retirement=defaults['salary_retirement'],
                down_payment=defaults['down_payment'],
                house_value=defaults['house_value'],    # This doesn't currently mean much since mortage=rent is fixed
                loan_term=defaults['loan_term'],
                age_purchase=defaults['age_purchase'],
                purchase_type=defaults['purchase_type'],
                age_social_security=defaults['age_social_security'],
                monthly_contribution_social_security=defaults['monthly_contribution_social_security']):

    ages = [x + age for x in range(age_death - age + 1)]
    years = [current_year]
    balances = []

    # TODO: Make home purchase and social security optional
    # TODO: Factor in taxes based on account type
    # TODO: Think through contribution/compounding periods and adjust accordingly
    for age in ages:
        years.append(years[-1] + 1)
        salary_retirement = salary_retirement * (1 + rate_inflation)
        if age == age_purchase:
            if purchase_type == "mortgage":
                savings_retirement = savings_retirement - down_payment
            elif purchase_type == "outright":
                savings_retirement = savings_retirement - house_value
        if age > age_purchase:
            house_value = house_value * (1 + rate_appreciation)
        if age_retirement > age > age_purchase + loan_term:
            savings_retirement = savings_retirement + 12 * rent
        if age < age_retirement:
            savings_retirement = savings_retirement * (1 + market_rate)
            savings_retirement = savings_retirement + 12 * contribution_monthly
        else:
            savings_retirement = savings_retirement * (1 + rate_retirement)
            savings_retirement = savings_retirement - salary_retirement
        if age > age_social_security:
            savings_retirement = savings_retirement + 12 * monthly_contribution_social_security
        if savings_retirement < 0:
            savings_retirement = 0
        balances.append(savings_retirement)

    return ages, balances


# Initialize the default values
initial_ages, initial_balances = recalculate()
initial_years = [x + current_year for x in range(len(initial_ages))]
initial_x_values = []
for initial_years_idx, initial_year in enumerate(initial_years):
    initial_x_values.append(f"{initial_year}, Age {initial_ages[initial_years_idx]}")

# TODO: Make the graph nicer
# TODO: highlight key moments/purchases/etc
# TODO: allow user to add multiple scenarios
# TODO: Have graphs of income/expenses and cross-filter/update with retirement balance graph
# TODO: Draw net worth (include assets/equity)

# Initialize the plotly/dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout = go.Layout(
    title='Retirement Balance over time',
    showlegend=True,
    legend=go.layout.Legend(
        x=0,
        y=1.0
    ),
    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
)

graph = dcc.Graph(
        id='retirement-bal-vs-time',
        figure={
            'data': [
                go.Scatter(
                    x=initial_ages,
                    y=initial_balances
                )
            ],
            'layout': layout
        },

    )

# Trying to keep this less verbose but there might be a better way since this requires formatting
children = [graph]
inputs = []
for key, value in defaults.items():
    label = key.replace('_', ' ')
    children.append(html.Label(label))
    input_id = key.replace('_', '-')
    inputs.append(Input(component_id=input_id, component_property='value'))
    if type(value) == int:
        children.append(dcc.Input(id=input_id, value=value, type='number'))
    else:
        children.append(dcc.Input(id=input_id, value=value, type='text'))

app.layout = html.Div(children, style={'columnCount': 2})


# This callback will cause the whole graph to redraw since technically it has new data
@app.callback(
    Output(component_id='retirement-bal-vs-time', component_property='figure'),
    inputs,
    [State('retirement-bal-vs-time', 'figure')]
)
def update_output_div(age_retirement, age, age_death, savings_retirement, market_rate, rate_retirement,
                      rate_appreciation, rate_inflation, contribution_monthly, rent, salary_retirement, down_payment,
                      house_value, loan_term, age_purchase, purchase_type, age_social_security,
                      monthly_contribution_social_security, figure):
    new_ages, new_balances = recalculate(age_retirement, age, age_death, savings_retirement, market_rate,
                                         rate_retirement,  rate_appreciation, rate_inflation, contribution_monthly,
                                         rent, salary_retirement, down_payment,  house_value, loan_term, age_purchase,
                                         purchase_type, age_social_security, monthly_contribution_social_security)
    new_years = [x + 2018 for x in range(len(new_ages))]
    new_x = []
    for index, new_year in enumerate(new_years):
        new_x.append(f"{new_year}\nAge {new_ages[index]}")
    figure['data'] = [{'x': new_ages, 'y': new_balances, 'type': 'scatter'}]
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
