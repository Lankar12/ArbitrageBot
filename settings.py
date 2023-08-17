from datetime import datetime

# Log files
LOG_FILE = 'logs.txt'

#config of prices and volumes
config = {
    'price_range': (20000, 50000),
    'volume_range': (1000, 10000),
    'start_date': datetime(2023, 1, 1),
    'end_date': datetime(2023, 1, 10),
    'frequency': '1H'
}

#fee in persentages
TRANSACTION_FEE = 0.01

# Maximum available amout for one operation
MAX_TRANSACTION_VOL = 500