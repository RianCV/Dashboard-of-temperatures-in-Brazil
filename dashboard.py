import base64
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

# Load and preprocess data

df = pd.read_csv("INMET_TOTAL/TOTAL_TOTAL/really_total_total.csv")
df["year"] = df.Period.str[:4]

temperatures_sum = df.Temperature.sum()
temperatures_max = df.Temperature.max()
temperatures_min = df.Temperature.min()

grouped_df = df.groupby("City")["Temperature"].sum().reset_index()
mean_of_sums = grouped_df.Temperature.mean().round()
temperatures_mean = df.Temperature.mean().round()


app = Dash(__name__)

app.layout = dcc.Tabs([
    dcc.Tab(label='Total Temperature', children=[
        html.Div([
            html.H1(children='Total Temperature', style={'textAlign': 'center'}),
            html.Label('Cidades'),
            dcc.Dropdown(df.City.unique(), ["ALEGRETE", "VACARIA"], multi=True, id="dropdown-selection_city_total"),
            dcc.Graph(id='graph-content_total'),
            dash_table.DataTable(id='data-table_total')
        ])
    ]),
    dcc.Tab(label='Temperature by Year', children=[
        html.Div([
            html.H1(children='Temperature by Year', style={'textAlign': 'center'}),
            dcc.Dropdown(df.City.unique(), ["ALEGRETE", "LAGES"], multi=True, id="dropdown-selection_city_year"),
            html.Label('Ano'),
            dcc.RadioItems(sorted(df.year.unique()), "2019", id='dropdown-selection_year', style={'padding': 10}),
            dcc.Graph(id='graph-content_year'),
            dcc.RangeSlider(1,12,1, value=[1,12], marks={
                1: 'jan',
                2: 'feb',
                3: 'mar',
                4: 'apr',
                5: 'may',
                6: 'jun',
                7: 'jul',
                8: 'aug',
                9: 'sep',
                10: 'oct',
                11: 'nov',
                12: 'dez',
            }, id='my-range-slider'),
            html.Br(),
            html.Br(),
            html.Br(),
            dash_table.DataTable(id='data-table_year')
        ])
    ]),
    dcc.Tab(label='Temperature by Year_BETA', children=[
        html.Div([
            html.H1(children='Temperature by Year BETA', style={'textAlign': 'center'}),
            dcc.Dropdown(df.City.unique(), ["ALEGRETE", "LAGES"], multi=True, id="dropdown-selection_city_season"),
            html.Label('Ano'),
            dcc.RadioItems(["Season 2019-2020", "Season 2020-2021", "Season 2021-2022", "Season 2022-2023"], "Season 2019-2020", id='dropdown-selection_season', style={'padding': 10}),
            dcc.Graph(id='graph-content_season'),
            html.Br(),
            html.Br(),
            html.Br(),
            dash_table.DataTable(id='data-table_season')
        ])
    ]),
    dcc.Tab(label="Raw Temperature Data", children=[
        html.Div([
            html.H1(children='Raw temperature by Year and City', style={'textAlign':'center'}),
            dcc.Dropdown(df.City.unique(), ["ALEGRETE"], multi=True, id="dropdown-selection_city"),
            dcc.Checklist(sorted(df.year.unique()), ['2019'],id='radioitem-selection_year', style={'display':'flex', 'margin':'1rem'}),
            html.H2(children="Table of temperatures:", style={'font-weight': 'normal'}),
            dash_table.DataTable(id='data-table')
        ]),
        html.Div([
            html.Button("Download this selected dataframe: ", id="btn_download"), dcc.Download(id="download-text-index")
        ])
    ])
])

##########       INICIO PRIMEIRA ABA        ################

@callback(
    Output('graph-content_total', 'figure'),
    Output('data-table_total', 'data'),
    Input('dropdown-selection_city_total', 'value')
)
def update_output_total(selected_city):
    dff = df[df.City.isin(selected_city)]
    fig = px.line(dff, x='Period', y='Temperature', color="City", title=f"Temperature of {', '.join(selected_city)}")
    grouped_df = dff.groupby('City')['Temperature'].agg(['mean', 'sum', 'max', 'min']).round().reset_index()
    last_line = {'City': 'TOTAL', 'mean': temperatures_mean, 'sum': mean_of_sums, 'max': temperatures_max, 'min': temperatures_min}
    grouped_df.loc[len(grouped_df)] = last_line
    return fig, grouped_df.to_dict('records')

##########       FIM PRIMEIRA ABA        ################


##########       INICIO SEGUNDA ABA        ################

@callback(
    Output('graph-content_year', 'figure'),
    Output('data-table_year', 'data'),
    Input('dropdown-selection_year', 'value'),
    Input('dropdown-selection_city_year', 'value'),
    Input('my-range-slider', 'value')
)
def update_output_year(selected_year, selected_city, selected_month):
    dff = df.copy()
    dff["month"] = dff['Period'].str[5:7].astype(int)
    dff = dff[(dff.year == selected_year) & (dff.City.isin(selected_city) & (dff.month >= selected_month[0]) & (dff.month <= selected_month[1]))]
    fig = px.line(dff, x='Period', y='Temperature', color="City", title=f"Temperature for {selected_year} in {', '.join(selected_city)}")
    grouped_df = dff.groupby(["City", "year"])["Temperature"].agg(["mean", "sum", "max", "min"]).reset_index()
    grouped_df["mean"] = grouped_df["mean"].round()
    return fig, grouped_df.to_dict('records')

##########       FIM SEGUNDA ABA        ################






##########       INICIO TERCEIRA ABA        ################

@callback(
    Output('graph-content_season', 'figure'),
    Output('data-table_season', 'data'),
    Input('dropdown-selection_season', 'value'),
    Input("dropdown-selection_city_season", 'value'),
)
def update_output_year(selected_season, selected_city):
    dff = df.copy()
    #dff["month"] = dff['Period'].str[5:7].astype(int)
    initial_year = selected_season[7:11]
    ended_year = selected_season[12:16]
    dff = dff[dff.year.isin([initial_year,ended_year]) & (dff.City.isin(selected_city))]

    dff['Period'] = pd.to_datetime(dff['Period'], format='%Y-%m')
    start_date = pd.to_datetime(f'{initial_year}-09', format='%Y-%m')
    end_date = pd.to_datetime(f'{ended_year}-09', format='%Y-%m')
    dff = dff[(dff['Period'] >= start_date) & (dff['Period'] <= end_date)]
    dff.Period = dff.Period.astype(str)


    fig = px.line(dff, x='Period', y='Temperature', color="City", title=f"Temperature for {selected_season} in {', '.join(selected_city)}")
    grouped_df = dff.groupby("City")["Temperature"].agg(["mean", "sum", "max", "min"]).reset_index()

    grouped_df["mean"] = grouped_df["mean"].round()
    return fig, grouped_df.to_dict('records')

##########       FIM TERCEIRA ABA        ################













##########       INICIO QUARTA ABA        ################
# EH SÓ CONCERTAR O CHECKLIST, SE NAO DER, VOLTA PRO RADIOITEM

@callback(
    Output('data-table', 'data'),
    Input('dropdown-selection_city', 'value'),
    Input('radioitem-selection_year', 'value'),
)

def uptdate_table(selected_city, selected_year):
    dff = df[(df.City.isin(selected_city)) & (df.year.isin(selected_year))]
    return dff.to_dict('records')

@callback(
        Output('download-text-index', 'data'),
        Input('radioitem-selection_year', 'value'),
        Input('dropdown-selection_city', 'value'),
        Input('btn_download', 'n_clicks')
)

def func(year, city, n_clicks):
    if n_clicks:
        dff = df[(df.year.isin(year)) & (df.City.isin(city))]
        csv_string = dff.to_csv(index=False, encoding='utf-8')
        b64 = base64.b64encode(csv_string.encode()).decode()
        return dict(content=b64, filename="dataframe.csv", base64=True)
    
##########       FIM QUARTA ABA        ################

if __name__ == '__main__':
    app.run_server(debug=True)
