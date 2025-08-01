<!-- ABOUT THE PROJECT -->
## About The Project

SMA backtest project, uses two tickers: one for signal and one to buy in the backtest. You can specify the day window

The program will output the backtest using different buffers for the SMA strategy and average that. Then, it will compare to a buy and hold the first ticker strategy.

<!-- GETTING STARTED -->
## Getting Started

Follow these instructions

Dependencies
* python
* yfinance
* pandas

1. Clone the repo
```sh
  git clone https://github.com/github_username/repo_name.git
  ```
2. Create a virtual environment
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment
   ```sh
   source venv/bin/activate
   ```
4. Install the requirements
   ```js
   pip install -r requirements.txt
   ```
5. Run the program
   ```sh
   python main.py
   ```
<!-- USAGE -->
## Usage

First ticker for SMA signal
Second ticker to actually buy and sell
Window input for SMA window(ex: 200d)

```sh
   First Ticker: SPY
   Second Ticker: SSO
   Window in days: 200d
```

<!-- ROADMAP -->
## Roadmap

- [X] Make it web based
- [ ] Update to include visualization

