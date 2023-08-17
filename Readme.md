# Arbitrage Bot

Arbitrage Bot is a Python-based application designed to simulate and analyze crypto trading using historical price data. This documentation will guide you through setting up and using the bot.

## Features
- Create a CSV file containing fictional price data within a specified range.
- Contrast prices from two exchanges and compute profits for the highest possible trading volume.
- Accommodates transaction fee percentages for exchange operations and a maximum volume threshold.
- Supports logs to record actions.
- Supports asynchronous execution for improved processing speed.
- Records events using a logging mechanism.
- Generates output results in a text file for further analysis.
- Provides a visualization that graphs price trends from both exchanges over time, pinpointing the most value potential arbitrage chances.


## Strategy
- Identify arbitrage opportunities, where the price of BTC on Exchange A is lower than on
Exchange B (taking into account a constant fee percentage for trading and transferring).
- Decide on a trading volume considering the volume available and a maximum cap.
Simulate the buying on Exchange A and selling on Exchange B, and vice versa.

## Prerequisites

- Python 3.x
- pandas
- numpy
- matplotlib
- and others

## Installation


Clone this repository:

```
git clone https://github.com/Lankar12/ArbitrageBot.git
cd ArbitrageBot
```

Install required dependencies:

```
pip install -r requirement.txt
```

## Usage

1. Open the `settings.py` file and set up the `TRANSACTION_FEE`, `MAX_TRANSACTION_VOL` and other values.

2. Run the bot:

```
python main.py
```

## Customization

You can customize the following parameters in the `settings.py` script inside config constant:

- `price_range`: The range of fictional prices.
- `volume_range`: The range of fictional volumes.
- `start_date`: The start date for generating price data.
- `end_date`: The end date for generating price data.
- `frequency`: The time between data points.

The bot will perform the arbitrage simulation for the specified exchange pairs and write the results to the `logs.txt` file.
Also you may see results inside console.