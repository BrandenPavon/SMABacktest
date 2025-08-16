import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from backtester import backtest
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO, template_from_url

load_figure_template(["bootstrap", "darkly"])
dbc_css = "dbc.min.css"

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

def returntickers():
    return ["QQQ", "QLD", "TQQQ", "SPY", "SSO", "UPRO"]

def load_d(ticker, ticker2, params):
    data = backtest(ticker, ticker2, f"{params["window"]}d", params)
    d1 = pd.read_csv(f"{ticker}_2024.csv", parse_dates=True, index_col=0)
    d1["Datetime"] = pd.to_datetime(d1.index)
    f1 = pd.DataFrame(data[0], columns=["Strategy"], index=d1["Datetime"])
    f2 = pd.DataFrame(data[1], columns=["Hold"], index=d1["Datetime"])
    f1["Date"] = pd.to_datetime(f1.index)
    f2["Date"] = pd.to_datetime(f2.index)
    frame = pd.merge(f1, f2, on="Date")
    return frame

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("SMABacktest", className="text-center text-primary mb-4"),
            width=12
        )
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Underlying Ticker", className="card-title"),
                    dcc.Dropdown(id="newtick", options=[{"label": t, "value": t} for t in returntickers()], value="QQQ", className="mb-3"),
                    html.H5("Trading Ticker", className="card-title"),
                    dcc.Dropdown(id="newtick2", options=[{"label": t, "value": t} for t in returntickers()], value="TQQQ", className="mb-3"),
                    #dcc.Dropdown(
                    #    id="newY",
                    #    options=[{"label": col, "value": col} for col in ["Adj Close", "Close", "High", "Low", "Open", "Volume"]],
                    #    value="Adj Close",
                    #    className="mb-3"
                    #),
                    html.H5("SMA Window in days", className="card-title"),
                    dbc.Input(id="window-input", type="number", value=200, placeholder="SMA Window", className="mb-2"),
                    html.H5("Buy Buffer in % (e.g 2%)", className="card-title"),
                    dbc.Input(id="buybuffer-input", type="number", value=2, placeholder="Buy buffer", className="mb-2"),
                    html.H5("Sell Buffer in % (e.g 2%)", className="card-title"),
                    dbc.Input(id="sellbuffer-input", type="number", value=2, placeholder="Sell buffer", className="mb-2"),
                    html.H5("Slippage rate in % (e.g 0.05%)", className="card-title"),
                    dbc.Input(id="slippage-input", type="number", value=0.05, placeholder="Slippage", className="mb-2"),
                    html.H5("Commission rate in % (e.g 0.05%)", className="card-title"),
                    dbc.Input(id="commrate-input", type="number", value=0.05, placeholder="Commission rate", className="mb-2"),
                ])
            ], className="mb-4"),
            md=4
        ),
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.DARKLY, dbc.themes.BOOTSTRAP], switch_props={"value": False}),
                    width="auto"
                ),
                justify="end"
            ),
            dcc.Graph(
                id="graph1",
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '75vh'}
            )
        ], md=8)
    ])
], fluid=True, className="dbc")

@app.callback(
    Output('graph1', 'figure'),
    [
        Input('newtick', 'value'),
        Input('newtick2', 'value'),
        Input('window-input', 'value'),
        Input('buybuffer-input', 'value'),
        Input('sellbuffer-input', 'value'),
        Input('slippage-input', 'value'),
        Input('commrate-input', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def update_graph(ticker, ticker2, window, buybuff, sellbuff, slip, commr, theme_toggle):
    wd = window 
    bb = buybuff
    sb = sellbuff
    sp = slip
    cr = commr 
    wd = wd if wd is not None else "200"
    bb = bb if bb is not None else "2"
    sb = sb if sb is not None else "2"
    sp = sp if sp is not None else "0.05"
    cr = cr if cr is not None else "0.05"
    df = load_d(ticker, ticker2, {
        "window": wd,
        "buy_buff": bb,
        "sell_buff": sb,
        "slippage": sp,
        "commrate": cr
    })
    # Determine the figure template based on the selected theme
    template_name = template_from_url(dbc.themes.DARKLY) if theme_toggle else template_from_url(dbc.themes.BOOTSTRAP)
    fig = px.line(df, x="Date", y=["Strategy", "Hold"], template=template_name)
    return fig

if __name__ == "__main__":
    app.run(debug=False)

