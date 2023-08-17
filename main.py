import pandas as pd
import csv
import logging
import matplotlib.pyplot as plt
import asyncio
from decimal import Decimal
from typing import List, Any

from logger import SetupLoger
from settings import LOG_FILE, TRANSACTION_FEE, MAX_TRANSACTION_VOL


class ArbitrageBot(SetupLoger):
    """
    Arbitrage trading bot for analyzing trading opportunities.

    This class represents an arbitrage trading bot that analyzes trading opportunities
    between two exchanges based on provided data.

    Args:
        src_data (str): The source data file containing trading information.
        transaction_fee (float): The transaction fee as a percentage.
        max_transaction_vol (float): The maximum transaction volume allowed.

    Attributes:
        transaction_fee (float): The transaction fee as a percentage.
        max_transaction_vol (float): The maximum transaction volume allowed.
        src_data (str): The source data file containing trading information.
    """

    def __init__(self, src_data: str, transaction_fee: float, max_transaction_vol: float):
        """
        Initialize the ArbitrageBot instance.

        Args:
            src_data (str): The source data file containing trading information.
            transaction_fee (float): The transaction fee as a percentage.
            max_transaction_vol (float): The maximum transaction volume allowed.
        """
        super().__init__()  # Call the constructor of the parent class
        self.transaction_fee = transaction_fee
        self.max_transaction_vol = max_transaction_vol
        self.src_data = src_data


    def calculate_profit(self, price_one: Decimal, price_two: Decimal, vol_one: Decimal,
                         vol_two: Decimal) -> Decimal:
        """
        Calculate the potential profit from a trade.

        This function calculates the profit that can be earned from a trade between two exchanges.

        Args:
            buyer_price (Decimal): The buying price from the first exchange.
            seller_price (Decimal): The selling price from the second exchange.
            vol_one (Decimal): Volume available for trading in the first exchange.
            vol_two (Decimal): Volume available for trading in the second exchange.

        Returns:
            Decimal: The calculated potential profit from the trade.
        """
        try:
            max_volume_to_trade = min(vol_one, vol_two, self.max_transaction_vol)
            buyer_price, seller_price = (price_one, price_two) if price_two > price_one \
                else (price_two, price_one)

            profit = (seller_price - buyer_price) * Decimal(max_volume_to_trade) * (
                        Decimal(1) - Decimal(self.transaction_fee))

            self.logger.info("Profit Calculation:")
            self.logger.info(f"Buyer Price: {buyer_price:.2f}")
            self.logger.info(f"Seller Price: {seller_price:.2f}")
            self.logger.info(f"Max Volume to Trade: {max_volume_to_trade:.2f}")
            self.logger.info(f"Transaction Fee: {self.transaction_fee:.2f}")
            self.logger.info(f"Calculated Profit: {profit:.2f}")

            return profit, max_volume_to_trade
        except Exception as e:
            self.logger.error(f"An error occurred while calculating profit: {str(e)}")
            return Decimal(0), Decimal(0)  # Return 0 in case of an error

    def add_trade_opportunities(self, trades: List[dict], data_entry: tuple) -> None:
        """
        Add trade opportunities to the list of trades.

        This method calculates the profit and maximum volume to trade for each opportunity
        and adds the trade opportunity to the list of trades.

        Args:
            trades (List[dict]): List of trade opportunity dictionaries.
            data_entry (tuple): Tuple containing trade data (timestamp, price_a, volume_a, price_b, volume_b).

        Returns:
            None
        """
        try:
            # Convert prices and volumes to Decimal
            timestamp = data_entry["Timestamp"]
            price_one = Decimal(data_entry["Exchange_price_one"])
            vol_one = Decimal(data_entry["Exchange_volume_one"])
            price_two = Decimal(data_entry["Exchange_price_two"])
            vol_two = Decimal(data_entry["Exchange_volume_two"])

            # Calculate profit and maximum volume to trade
            profit, max_volume_to_trade = self.calculate_profit(price_one, price_two, vol_one, vol_two)

            # Create a trade opportunity dictionary
            trade = {
                'timestamp': timestamp,
                'exchange1': price_one,
                'exchange2': price_two,
                'vol': max_volume_to_trade,
                'profit': profit
            }

            # Append the trade opportunity to the list of trades
            trades.append(trade)

            self.logger.info(f"Added trade opportunity: Timestamp: {timestamp}, Profit: {profit:.2f}")

        except Exception as e:
            self.logger.error(f"An error occurred while adding trade opportunity: {str(e)}")

    async def get_arbitrage_opportunities(self) -> List[dict]:
        """
        Find arbitrage trade opportunities.

        This function scans the provided data file for potential arbitrage trade opportunities
        and returns a list of these opportunities.

        Returns:
            List[dict]: A list of trade opportunity objects representing the identified arbitrage trade opportunities.
        """
        trade_opportunities = []

        with open(self.src_data, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                self.add_trade_opportunities(trade_opportunities, row)

        return trade_opportunities

    @staticmethod
    def display_trade_summary(trade_opportunities: List[dict], logger: Any) -> None:
        """
        Display a summary of trade opportunities.

        Args:
            trade_opportunities (List[dict]): List of trade opportunity information dictionaries.
            logger: The logger instance to log the trade summary.
        """
        total_profit = sum(trade['profit'] for trade in trade_opportunities)
        total_trades = len(trade_opportunities)

        logger.info("Trading Summary:")
        logger.info(f"Total Profit: {total_profit:,.2f}")
        logger.info(f"Total trade opportunities: {total_trades}")

    @staticmethod
    def display_trade_details(trade_opportunities: List[dict], logger: Any) -> None:
        """
        Display details of each trade opportunity.

        Args:
            trade_opportunities (List[dict]): List of trade opportunity information dictionaries.
            logger: The logger instance to log trade opportunity details.
        """
        logger.info("Trading opportunities:")
        for trade in trade_opportunities:
            logger.info(f"Timestamp: {trade['timestamp']}")
            logger.info(f"Exchange 1 Price: {trade['exchange1']:.2f}")
            logger.info(f"Exchange 2 Price: {trade['exchange2']:.2f}")
            logger.info(f"Transaction Volume: {trade['vol']:.2f}")
            logger.info(f"Profit Earned: {trade['profit']:.2f}")
            logger.info('*' * 50)

    @staticmethod
    def plot_trade_profit_over_time(trade_opportunities: List[dict]) -> None:
        """
        Plot trade profits and highlight top 10% arbitrage opportunities over time.

        Args:
            trade_opportunities (List[dict]): List of trade opportunity dictionaries.

        Returns:
            None
        """
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(trade_opportunities)

        # Extract data for plotting
        timestamps = pd.to_datetime(df['timestamp'])
        exchange1_prices = df['exchange1'].apply(Decimal)
        exchange2_prices = df['exchange2'].apply(Decimal)

        # Sort the trade opportunities by profit in descending order
        trade_opportunities.sort(key=lambda trade: trade['profit'], reverse=True)

        # Calculate the number of opportunities to highlight (top 10%)
        num_to_highlight = int(len(trade_opportunities) * 0.1)

        # Plot the prices from both exchanges
        plt.figure(figsize=(10, 6))
        plot1, = plt.plot(timestamps, exchange1_prices, label='Exchange 1')
        plot2, = plt.plot(timestamps, exchange2_prices, label='Exchange 2')

        # Highlight the top 10% arbitrage opportunities
        for trade in trade_opportunities[:num_to_highlight]:
            timestamp = trade['timestamp']
            profit = trade['profit']
            opportunity_timestamp = pd.to_datetime(timestamp)

            plt.axvline(x=opportunity_timestamp, color='r', linestyle='--', label=f'Profit (+{profit:.2f})')

        # Create a custom legend entry for the red dashed line
        custom_legend_entry = plt.Line2D([0], [0], color='r', linestyle='--', label=f'Profit')

        # Combine all legend entries
        handles = [plot1, plot2, custom_legend_entry]
        labels = [h.get_label() for h in handles]


        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.title('Prices from Both Exchanges Over Time')
        plt.legend(handles=handles, labels=labels, loc='upper left', bbox_to_anchor=(1, 1))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

async def main() -> None:
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    pairs_to_monitor = [
        ('generated_fictional_prices.csv', TRANSACTION_FEE, MAX_TRANSACTION_VOL)
        # Add more pairs if needed
    ]

    tasks = []
    for pair_info in pairs_to_monitor:
        bot = ArbitrageBot(pair_info[0], pair_info[1], pair_info[2])
        tasks.append(bot.get_arbitrage_opportunities())

    all_trades = await asyncio.gather(*tasks)
    trades = all_trades[0]

    bot.display_trade_details(trades, bot.logger)
    bot.display_trade_summary(trades, bot.logger)
    bot.plot_trade_profit_over_time(trades)


if __name__ == '__main__':
    asyncio.run(main())
