import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


class MyInput:
    def __init__(self, input_id, name, tooltip_text, value, input_type="number", step=1):
        self.input_id = input_id
        self.name = name
        self.tooltip_text = tooltip_text
        self.value = value
        self.input_type = input_type
        self.step = step
        self.label = html.Label(name)
        self.user_input = dcc.Input(id=input_id, value=value, type=input_type, step=step)
        self.callback_input = Input(component_id=input_id, component_property='value')
        self.tooltip = html.Abbr("\u003F", title=tooltip_text)
        self.container = html.Div(children=[self.label, self.user_input, self.tooltip])


now = datetime.datetime.now()
current_year = now.year


def recalculate(input_dict):
    age_retirement = input_dict["age-retirement"].value
    age = input_dict["age-current"].value
    age_death = input_dict["age-death"].value
    savings_retirement = input_dict["savings-retirement"].value
    market_rate = float(input_dict["rate-market"].value) / 100
    rate_retirement = float(input_dict["rate-retirement"].value) / 100
    rate_inflation = float(input_dict["rate-inflation"].value) / 100
    contribution_monthly = input_dict["contribution-monthly"].value
    salary_retirement = input_dict["salary-retirement"].value
    age_social_security = input_dict["age-social-security"].value
    monthly_contribution_social_security = input_dict["contribution-monthly-social-security"].value
    
    ages = [x + age for x in range(age_death - age + 1)]
    years = [current_year]
    balances = []

    for age in ages:
        years.append(years[-1] + 1)
        salary_retirement = salary_retirement * (1 + rate_inflation)
        if age < age_retirement:
            savings_retirement = savings_retirement * (1.0 + market_rate)
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


inputs = [
    MyInput("age-current", "Age", "Your current age", 32),
    MyInput("age-retirement", "Retirement Age", "The age you expect to retire", 65),
    MyInput("age-death", "Age of Death", "The age to which you expect to live", 80),
    MyInput("savings-retirement", "Current Retirement Savings", "Your primary retirement savings balance", 10000),
    MyInput("rate-retirement", "Retirement Rate",
            "The estimated earnings rate of your retirement fund DURING retirement", 3),
    MyInput("rate-market", "Market Rate",
            "The estimated earnings rate of your retirement fund BEFORE retirement",  7, 0.01),
    MyInput("rate-inflation", "Inflation Rate", "The estimated average inflation rate", 3.22, 0.01),
    MyInput("contribution-monthly", "Monthly Contribution",
            "The amount you contribute to your retirement fund each month", 200),
    MyInput("salary-retirement", "Desired Retirement Salary", "The annual amount you need to live during retirement",
            27500),
    MyInput("age-social-security", "Social Security Collection Age",
            "The age at which you plan to begin collecting social security", 65),
    MyInput("contribution-monthly-social-security", "Monthly Social Security",
            "The monthly amount you expect to receive from social security", 3698)
]

input_dict = {}
for input_item in inputs:
    input_dict[input_item.input_id] = input_item

input_containers = [my_input.container for my_input in inputs]
callback_inputs = [my_input.callback_input for my_input in inputs]

initial_ages, initial_balances = recalculate(input_dict)

# Initialize the plotly/dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

application = app.server

layout = go.Layout(
    title='Retirement Balance Over Time',
    showlegend=False,
    margin=go.layout.Margin(l=40, r=0, t=40, b=30),
    xaxis=dict(title='Age'),
    yaxis=dict(title='USD')
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


app.layout = html.Div(children=[
    html.Div([graph], style={'width': '100%'}),
    html.Div(input_containers, style={'columnCount': 2})]
)


def get_new_figure(input_dict, figure):
    new_ages, new_balances = recalculate(input_dict)
    figure['data'] = [{'x': new_ages, 'y': new_balances, 'type': 'scatter'}]
    return figure


# Warning: Assumes inputs list and callback input arguments are received in the same order
def update_inputs(input_values):
    for i, my_input in enumerate(inputs):
        my_input.value = input_values[i]


@app.callback(
    Output(component_id='retirement-bal-vs-time', component_property='figure'),
    callback_inputs,
    [State('retirement-bal-vs-time', 'figure')]
)
def update_output_div(*input_values):
    update_inputs(input_values)
    figure = input_values[-1]
    return get_new_figure(input_dict, figure)


if __name__ == '__main__':
    application.run(debug=True, port=8080)
