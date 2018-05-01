import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()

df = pd.read_csv('C:\\Users\\jdoering\\Desktop\\tmp\\copy\\dash\\dash_tutorials\\example_data\\gdp-life-exp-2007.csv')

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]

app.layout = html.Div(className = "wrapper",
    children = [
    html.Div(className="box a",
      children = [
          html.Div(className = "box aa",
                children = [
                    dcc.Dropdown(
                    # select Quater
                        id = 'quarter_select',
                        options=[
                            {'label': 'QT4 2018', 'value': 'NYC'},
                            {'label': 'QT3 2018', 'value': 'MTL'},
                            {'label': 'QT2 2018', 'value': 'SF'},
                            {'label': 'QT1 2018', 'value': 'SF'},
                        ],
                        value='NYC'
                    ),
                    dcc.Dropdown(
                        id = 'company_select',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        value='MTL'
                    )]),

           html.Div(className = "box ac",
                children=[
                    #Markdown
                    html.Div(
                      id='company_information',
                        style = {'hight' : '80%'}
                  )])
          ]),

    html.Div(className="box b",
              children=[
              dcc.Graph(
                  id='d2',
                  figure={
                      'data': [
                          go.Bar(
                              x=[-10, 20, 30, 40, -50, 40],
                              y=['A', 'B', 'C','D', 'E', 'F'],
                              orientation = 'h')
                      ]
                  }
              )
          ]),

    html.Div(className="box c",
              children=[
              dcc.Graph(
                  id='d3',
                  figure={
                      'data': [
                          go.Pie(
                                labels = ['EFSS','Meta Data Mngm','Data Gov', 'Data Prep', 'Information'],
                                values = [4.5, 7.5, 7.6, 3.9, 7.6])
                      ]
                  },
              )
          ]),

    html.Div(className="box d",
        children=[
            html.Div(className="container",
            children=[dt.DataTable(
                    rows=DF_GAPMINDER.to_dict('records'),

                    # optional - sets the order of columns
                    columns=sorted(DF_GAPMINDER.columns),
                    row_selectable=False,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='datatable-gapminder',
                    editable=False
                )])
        ]),

    html.Div(className="box e",
        children=[dcc.Graph(id='indicator-graphic')])
    ])


@app.callback(
    Output(component_id='company_information', component_property='children'),
    [Input(component_id='company_select', component_property='value')]
)


def update_company_div(input_val):
    string = """
    {}""".format(input_val)
    return dcc.Markdown(string)

# additional
app.css.append_css({
    'external_url': 'https://codepen.io/jondoering/pen/ZoEZxY.css'
})


if __name__ == '__main__':
    app.run_server(port=8060)
