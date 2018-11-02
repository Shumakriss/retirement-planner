import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    html.Label("Appreciation Rate"),
    dcc.Input(id='appreciation-rate', value=3.7, type='text'),
    html.Label("Mortage Rate"),
    dcc.Input(id='mortgage-rate', value=4.9, type='text'),
    html.Label("Market Rate"),
    dcc.Input(id='market-rate', value=10, type='text'),
    html.Label("Interest Rate During Retirement"),
    dcc.Input(id='retirement-rate', value=3, type='text'),
    html.Label("Inflation Rate"),
    dcc.Input(id='inflation-rate', value=3.22, type='text'),
    html.Label("Current Age"),
    dcc.Input(id='current-age', value=30, type='text'),
    html.Label("Retirement Salary"),
    dcc.Input(id='retirement-salary', value=50000, type='text'),
    html.Label("Total Savings"),
    dcc.Input(id='starting-amount', value=285000, type='text'),
    html.Label("Current rent"),
    dcc.Input(id='current-rent', value=2200, type='text'),
    html.Label("Current monthly savings"),
    dcc.Input(id='monthly-savings', value=800, type='text'),
    html.Label("Cash allocated for home purchase"),
    dcc.Input(id='cash-allocated', value=125000, type='text'),
    html.Label("Age of death"),
    dcc.Slider(
        id='death-slider',
        min=65,
        max=115,
        marks={65: "65", 90: "90", 115: "115"},
        value=75,
    ),
    html.Div(id='death-slider-output-container'),
    html.Label("Age of retirement"),
    dcc.Slider(
        id='retirement-slider',
        min=30,
        max=100,
        marks={30: "30", 65: "65", 100: "100"},
        value=60,
    ),
    html.Div(id='retirement-slider-output-container'),
])


@app.callback(
    dash.dependencies.Output('death-slider-output-container', 'children'),
    [dash.dependencies.Input('death-slider', 'value')])
def update_output(value):
    return '{}'.format(value)


@app.callback(
    dash.dependencies.Output('retirement-slider-output-container', 'children'),
    [dash.dependencies.Input('retirement-slider', 'value')])
def update_output(value):
    return '{}'.format(value)


if __name__ == '__main__':
    app.run_server()