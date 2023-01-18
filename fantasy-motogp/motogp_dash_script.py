import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# url = "https://www.motogp.com/en/gp-results/2022/QAT/MotoGP/RAC/Classification"
url = "https://en.wikipedia.org/wiki/2022_MotoGP_World_Championship"

# page = requests.get(url)
data = requests.get(url).text

# soup = BeautifulSoup(page.content, "html.parser")
soup = BeautifulSoup(data, "html.parser")

dfs = pd.read_html(url, attrs = {'class': 'wikitable'},  flavor='bs4', thousands ='.')
df = dfs[5]
df1 = df.iloc[:, :4]
df2 = df.iloc[:, 4:].replace(r'\D+', "", regex=True).replace(r'^\s*$', np.nan, regex=True).fillna(25).astype(int)
df3 = pd.concat([df1, df2], axis=1)
df4 = df3.drop(["Pos.", "Bike", "Team", "Pts"], axis=1).set_index("Rider").drop("Rider").T
df4.index.names = ['Track']
df5 = df4.reset_index()

del df5["Stefan Bradl"]
del df5["Tetsuta Nagashima"]

points_csv = pd.read_csv("C:/Users/ckhan/Documents/coding_projects/scraping_websites/motogp/data/championship_points_mapping.csv")
points_map = dict(points_csv.values)

def pts_fn(x):
    if int(x) in points_map.keys():
        return points_map[int(x)]
    else:
        return 0

df6 = pd.DataFrame()

df6["Track"] = df5["Track"]

for rider in df5.columns[1:]:
    df6[f"{rider}_points"] = df5[rider].map(lambda x: pts_fn(x))
    df6[f"{rider}"] = df6[f"{rider}_points"].cumsum()
    del df6[f"{rider}_points"]

fig1 = px.line(
                df5, 
                x=df5["Track"], 
                y=df5.columns[1:], 
                template="plotly_dark",
                labels={
                    "Track": "Track",
                    "value": "Position",
                    "variable": "Rider"
                    },
                title="MotoGp Rider Position 2022",
            )

fig1['layout']['yaxis']['autorange'] = "reversed"

fig2 = px.line(
                df6, 
                x=df6["Track"], 
                y=df6.columns[1:], 
                template="plotly_dark",
                labels={
                    "Track": "Track",
                    "value": "Points Total",
                    "variable": "Rider"
                    },
                title="MotoGp Cumulative Points 2022",
            )

# fig1.update_layout(height=700)

# fig2.update_layout(height=600)

dark_theme = {
    "main-background": "#000000",
    "header-text": "#ff7575",
    "sub-text": "#ffd175",
}

import dash
from dash import html, dcc
# from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        # html.H1(children='MotoGp Rider Position 2022', style={'backgroundColor':'black', "sub-text": "white"}),

        # html.Div(children='''
        #     Dash: A web application framework for Python.
        # '''),

        dcc.Graph(
            id='graph1',
            figure=fig1
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        # html.H1(children='MotoGp Cumulative Points 2022', style={'backgroundColor':'black', "sub-text": "white"}),

        html.Div(style={'backgroundColor':'black', "header-text": "white"}),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


