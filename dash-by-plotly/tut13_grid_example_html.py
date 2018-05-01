import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import flask
import os




dcc._css_dist[0]['relative_package_path'].append('grid_dash.css')
df = pd.read_csv('.\example_data\gdp-life-exp-2007.csv')

app = dash.Dash()

app.layout = html.Div([

    # line 1
    html.Div(children=[dcc.Graph(
            id='id1',
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
            },

        )],
        className='grid-item'),
    html.Div(children=[dcc.Graph(
        id='id2',
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
        },

    )],
        className='grid-item'),
    html.Div(children=[dcc.Graph(
        id='id3',
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
        },

    )],
        className='grid-item'),
    html.P('Example P', className='grid-item', id='my-p-element')

],
    className ='grid-container')

# app.layout = html.Div([
#     html.Div('1', className = "grid-item"),
#     html.Div('2', className = "grid-item"),
#     html.Div('3', className = "grid-item"),
#     html.Div('4', className = "grid-item"),
#     html.Div('5', className = "grid-item"),
#     html.Div('6', className = "grid-item"),
#     html.Div('7', className = "grid-item"),
#     html.Div('8', className = "grid-item"),
#     html.Div('9', className = "grid-item")
#     ],
#     className = "grid-container"
# )

app.css.append_css({
    'external_url': 'https://codepen.io/jondoering/pen/MGWqrW.css'
})

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

if __name__ == '__main__':
    app.run_server(debug=True)