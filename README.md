<!-- ABOUT THE PROJECT -->
## About The Project

SMA backtest project, uses two tickers: one for signal and one to buy in the backtest. You can specify the day window

The program will output the backtest visualized with a graph using different buffers for the SMA strategy and average that. Then, it will compare to a buy and hold the first ticker strategy.


![My Remote Image](https://bpsite.xyz/static/smabacktest1.png)

<!-- GETTING STARTED -->
## Getting Started

Follow these instructions

Dependencies
* python3.13

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

First input buy buffer in percentage (ex: 2%)
Second input sell buffer in percentage (ex: 2%)
Third input slippage rate in percentage (ex: 0.05%)
Fourth input commission rate in percentage (ex: 0.01%)

<!-- ROADMAP -->
## Roadmap

- [X] Make it web based
- [X] Update to include visualization
- [X] Include commission and slippage rate in user input
- [X] Make it pretty
- [ ] Implement OOP
- [ ] Include a file that allows users to choose custom ticker symbols

