
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np


app = dash.Dash()

df = pd.read_csv('.\example_data\gdp-life-exp-2007.csv')


# create graphs
def scatter_plot(id):
    figure = dcc.Graph(
            id = id,
            figure = {
                'data' : [
                    go.Scatter(
                        x=df['life expectancy'],
                        y=df['gdp per capita'],
                        mode='markers'                                     #makes it a scatter
                    )
                    ],
                'layout': go.Layout(
                    xaxis={'type' : 'log', 'title' : 'Xtitle'},
                    yaxis={'title' : 'YTitle'},
                    hovermode='closest'
                )
            }
        )

    return figure

def line_plot(id):
# https://plot.ly/python/line-charts/
    figure = dcc.Graph(
        id = id,
        figure = {
            'data' : [
                go.Scatter(
                    x = df['life expectancy'].sort_values(),
                    y =  range(df.shape[0]),
                    mode='lines'                                            #makes it a line plot
                )],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Xtitle'},
                yaxis={'title': 'YTitle'},
                hovermode='closest'
                )
        }
    )

    return figure

def pie_plot(id):
# https://plot.ly/python/pie-charts/
    figure = dcc.Graph(
        id = id,
        figure = {
            'data' : [
                go.Pie(
                    labels = ['EFSS','Meta Data Mngm','Data Gov', 'Data Prep', 'Information'],
                    values = [4.5, 7.5, 7.6, 3.9, 7.6]
                )]
        }
    )

    return figure

def bar_plot(id):
# https://plot.ly/python/bar-charts/

    figure = dcc.Graph(
        id = id,
        figure = {
            'data' : [
                go.Bar(
                    x=['giraffes', 'orangutans', 'monkeys'],
                    y=[20, 14, 23]
                )]
        }
    )

    return figure

# ------
app.layout = html.Div([

        # line one
        html.Div([
            html.Div([
                scatter_plot('scatter_1')],
                style = {'width': '48%', 'display': 'inline-block'}),

            html.Div([
                line_plot('line_1')],
                style = {'width': '48%', 'display': 'inline-block'})
                ]),

        # line two
        html.Div([

            html.Div([
                bar_plot('bar_id')],
                style = {'width' : '48%', 'display' : 'inline-block'}
            ),
            html.Div([
                pie_plot('pie_id')],
                style = {'width' : '48%', 'display' : 'inline-block'}
            )
        ])
])

# ------

if __name__ == '__main__':
    app.run_server()