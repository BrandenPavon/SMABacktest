import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

def load_d(ticker: str, ticker2: str):
    data1 = pd.read_csv(f"{ticker}_2024.csv", parse_dates=True, index_col=0)
    data2 = pd.read_csv(f"{ticker2}_2024.csv", parse_dates=True, index_col=0)
    data1["Datetime"] = pd.to_datetime(data1.index)
    data2["Datetime"] = pd.to_datetime(data2.index)
    data = pd.merge(data1, data2, on="Datetime")
    options = ["Adj Close", "Close", "High", "Low", "Open", "Volume"]
    for option in options:
        data[f"{option} {ticker}"] = data[f"{option}_x"]
        data[f"{option} {ticker2}"] = data[f"{option}_y"]
    return data 

app.layout = html.Div([
    html.Div(children="test"),
    dcc.Dropdown(id="newtick", options=["QQQ", "QLD", "TQQQ", "SPY", "SSO", "UPRO"], value="QQQ", placeholder="QQQ"),
    dcc.Dropdown(id="newtick2", options=["QQQ", "QLD", "TQQQ", "SPY", "SSO", "UPRO"], value="TQQQ", placeholder="TQQQ"),
    dcc.Dropdown(id="newY", options=["Adj Close", "Close", "High", "Low", "Open", "Volume"], value="Adj Close", placeholder="Adj Close"),
    #dcc.Graph(animate=True, id="graph1", animation_options={ "frame" : { "redraw" : True}, "transition": {"duration": 5, "ease": "linear"}}),
    dcc.Graph(figure={}, id="graph1"),
])

@app.callback(
    Output('graph1', 'figure'),
    Input('newtick', 'value'),
    Input('newtick2', 'value'),
    Input('newY', 'value')
)
def update_ticker(ticker: str, ticker2: str, newYval: str):
    fig = px.line(data_frame=load_d(ticker, ticker2), x="Datetime", y=[f"{newYval} {ticker}", f"{newYval} {ticker2}"])
    return fig

if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.run()
