# Arbitrage Bot

Arbitrage Bot is a Python-based application designed to simulate and analyze crypto trading using historical price data. This documentation will guide you through setting up and using the bot.


## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#getting-started)
- [Usage](#usage)
- [Features](#featuers)
- [Asynchronous Launch](#asynchronous-launch)

## Introduction
- Identify arbitrage opportunities, where the price on Exchange A is lower than on
Exchange B (taking into account a constant fee percentage for trading and transferring).
- Decide on a trading volume considering the volume available and a maximum cap.
Simulate the buying on Exchange A and selling on Exchange B, and vice versa.

## Prerequisites

- Python 3.x
- pandas
- numpy
- matplotlib
- and others (specified in requirements.txt)

## Installation

### Clone this repository:


```bash
git clone https://github.com/Lankar12/ArbitrageBot.git
cd ArbitrageBot
```

### Install required dependencies:

```
pip install -r requirement.txt
```

## Usage

1. Open the `settings.py` file and set up the constants(`config`, `TRANSACTION_FEE`, `MAX_TRANSACTION_VOL`).
2. Generate simulated data:

```
python generate_fiction_data.py
```
3. Run the bot:
```
python main.py
```


## Features
- Create a CSV file containing fictional price data within a specified range.
- Compare prices from two exchanges to calculate potential profits based on the highest achievable trading volume..
- Account for transaction fees in exchange operations and set a maximum volume threshold.
- Log events using a built-in logging mechanism.
- Execute operations asynchronously to improve processing speed.
- Generate output results in a text file for further analysis.
- Visualize price trends from both exchanges over time, highlighting potential arbitrage opportunities.


The bot will simulate arbitrage for the specified exchange pairs and write the results to the logs.txt file. 
The visualization includes two graphs with vertical lines indicating potentially profitable deals. 
The results will also be displayed in the console.

## Asynchronous Launch

For running this code asynchronously. We need to generate several files and put inside with fee and volume
```python     
pairs_to_monitor = [
        ('generated_fictional_prices.csv', TRANSACTION_FEE, MAX_TRANSACTION_VOL)
        # Add more pairs if needed
        ]
```
