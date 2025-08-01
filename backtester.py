import yfinance as yf
import os
import pandas as pd

def backtest(tick1: str, tick2: str, win: str):
    print(f"BACKTEST FOR {tick1} & {tick2}")
    if not os.path.exists(f"{tick1}_2024.csv"):
        yf.download(f"{tick1}", start="2014-01-01", end="2025-07-01", auto_adjust=False, multi_level_index=False).to_csv(f'{tick1}_2024.csv', index=True)
    if not os.path.exists(f"{tick2}_2024.csv"):
        yf.download(f"{tick2}", start="2014-01-01", end="2025-07-01", auto_adjust=False, multi_level_index=False).to_csv(f'{tick2}_2024.csv', index=True)
    df = pd.read_csv(f"{tick1}_2024.csv", parse_dates=True, index_col=0)
    df2 = pd.read_csv(f"{tick2}_2024.csv", parse_dates=True, index_col=0)
    df["SMA"] = df["Adj Close"].rolling(window=win).mean()
    money = 0
    shares = 0
    latestcloseprice = 0
    buffer = 0.0
    commission_rate = 0.001
    slippage_rate = 0.0005
    holdshares = 100/df.head(n=1)["Adj Close"].item()
    totalportval = 0
    totalportreturn = 0
    totalcagr = 0
    for i in range(10):
        money = 100
        shares = 0
        wintrades = 0
        prevportval = 0
        trades = 0
        latestcloseprice = 0
        totalprofit = 0
        totalloss = 1
        profitfactor = 0
        indexnum = 0
        for row, row2 in zip(df.itertuples(), df2.itertuples()):
            if (row._1 > row.SMA*(1+buffer)):
                if (money > 0):
                    adjusted_price = row2._1 * (1 + slippage_rate)
                    trade_value = money * (1 - commission_rate)
                    shares = trade_value / adjusted_price
                    prevportval = money
                    money = 0
                    trades += 1
            elif (row._1 < row.SMA*(1-buffer)):
                if (shares > 0):
                    adjusted_price = row2._1 * (1 - slippage_rate)
                    trade_value = shares * adjusted_price * (1 - commission_rate)
                    money = trade_value
                    if (prevportval < money):
                        wintrades += 1
                        totalprofit += money - prevportval
                    if (prevportval > money):
                        totalloss += prevportval - money
                    prevportval = money
                    shares = 0
                    trades += 1
            latestcloseprice = row2._1 
            portval = money + shares * latestcloseprice
        portreturn = (portval-100)/100
        CAGR = ((portreturn) ** (1/11.5) - 1)*100
        totalportval += portval
        totalportreturn += portreturn
        totalcagr += CAGR
        expectancy = ((wintrades/trades) * (totalprofit/trades)) - ((1-(wintrades/trades))* (totalloss/trades))
        print(f'Portfolio value is ${portval:.2f}, buffer: {buffer:.3f}, CAGR: {CAGR:.2f}%, Trades: {trades}, Return: {portreturn*100:.2f}%')
        print(f'Win rate is ${100*(wintrades/trades):.2f}%, expectancy: {expectancy:.2f}, profitfactor: {totalprofit/totalloss:.2f}')
        print('------')
        buffer += 0.005
    holdportval = holdshares * df.tail(n=1)["Adj Close"].item()
    print(f'The average portfolio value is ${totalportval/10:.2f}, CAGR: {totalcagr/10:.2f}%, Return: {totalportreturn*10:.2f}%')
    print(f'Holding would have gave Portfolio value: ${holdportval: .2f}, CAGR: {((holdportval/ 100) ** (1/11.5) - 1)*100}%, Return: {(holdportval-100):.2f}%')

def main():
    while True:
        backtest(input("Enter First Ticker: "), input("Enter Second Ticker: "), input("SMA Window (ex: 200d): "))

if __name__ == "__main__":
    main()
