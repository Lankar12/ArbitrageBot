import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import logging

from logger import SetupLoger
from settings import config, LOG_FILE

class CryptoPriceGenerator(SetupLoger):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()  # Call the constructor of the parent class
        self.start_date: datetime = config['start_date']
        self.end_date: datetime = config['end_date']
        self.frequency: str = config['frequency']
        self.price_range: tuple = config['price_range']
        self.volume_range: tuple = config['volume_range']

    def generate_price_data(self) -> pd.DataFrame:
        try:
            timestamps = pd.date_range(start=self.start_date, end=self.end_date, freq=self.frequency)
            num_timestamps: int = len(timestamps)

            data: Dict[str, List[Any]] = {
                'Timestamp': timestamps,
                'Exchange_price_one': np.random.uniform(self.price_range[0], self.price_range[1] + 1, num_timestamps),
                'Exchange_volume_one': np.random.uniform(self.volume_range[0], self.volume_range[1] + 1, num_timestamps),
                'Exchange_price_two': np.random.uniform(self.price_range[0], self.price_range[1] + 1, num_timestamps),
                'Exchange_volume_two': np.random.uniform(self.volume_range[0], self.volume_range[1] + 1, num_timestamps)
            }

            df: pd.DataFrame = pd.DataFrame(data)
            self.logger.info(f"File is created")
            return df

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Set up logging for the main function
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    crypto_price_generator: CryptoPriceGenerator = CryptoPriceGenerator(config)
    fictional_data: pd.DataFrame = crypto_price_generator.generate_price_data()

    if not fictional_data.empty:
        output_file: str = 'generated_fictional_prices.csv'
        fictional_data.to_csv(output_file, index=False)
        print(f"The data is created '{output_file}'.")
