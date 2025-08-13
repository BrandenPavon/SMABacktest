import dash
from backtester import backtest
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

def returntickers():
    return ["QQQ", "QLD", "TQQQ", "SPY", "SSO", "UPRO"]

def load_d(ticker: str, ticker2: str, params: dict):
    d1 = pd.read_csv(f"{ticker}_2024.csv", parse_dates=True, index_col=0)
    d1["Datetime"] = pd.to_datetime(d1.index)
    data = backtest(ticker, ticker2, "200d", params)
    frame1 = pd.DataFrame(data[0], columns=["Strategy"], index=d1["Datetime"])
    frame2 = pd.DataFrame(data[1], columns=["Hold"], index=d1["Datetime"])
    frame1["Date"] = pd.to_datetime(frame1.index)
    frame2["Date"]= pd.to_datetime(frame2.index)
    print(frame1)
    print(frame2)
    frame = pd.merge(frame1, frame2, on="Date")
    return frame 

app.layout = html.Div([
    html.Div(children="test"),
    dcc.Dropdown(id="newtick", options=returntickers(), value="QQQ", placeholder="QQQ"),
    dcc.Dropdown(id="newtick2", options=returntickers(), value="TQQQ", placeholder="TQQQ"),
    dcc.Dropdown(id="newY", options=["Adj Close", "Close", "High", "Low", "Open", "Volume"], value="Adj Close", placeholder="Adj Close"),
    dcc.Input(
        id="buybuffer-input",
        type="number",
        value="2",
        placeholder="2"
    ),
    dcc.Input(
        id="sellbuffer-input",
        type="number",
        value="2",
        placeholder="2"
    ),
    dcc.Input(
        id="slippage-input",
        type="number",
        value="0.05",
        placeholder="0.05"
    ),
    dcc.Input(
        id="commrate-input",
        type="number",
        value="0.05",
        placeholder="0.05"
    ),
    #dcc.Graph(animate=True, id="graph1", animation_options={ "frame" : { "redraw" : True}, "transition": {"duration": 5, "ease": "linear"}}),
    dcc.Graph(figure={}, id="graph1"),
])

@app.callback(
    Output('graph1', 'figure'),
    Input('newtick', 'value'),
    Input('newtick2', 'value'),
    Input('buybuffer-input', 'value'),
    Input('sellbuffer-input', 'value'),
    Input('slippage-input', 'value'),
    Input('commrate-input', 'value')
)
def update_ticker(ticker: str, ticker2: str, buybuff: str, sellbuff: str, slip: str, cr: str):
    fig = px.line(data_frame=load_d(ticker, ticker2, {"buy_buff": buybuff, "sell_buff": sellbuff, "slippage": slip, "commrate": cr}), x="Date", y=["Strategy", "Hold"])
    return fig

if __name__ == "__main__":
    app.run()
