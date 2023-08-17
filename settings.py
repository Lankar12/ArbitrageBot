from datetime import datetime

# Log files
LOG_FILE = 'logs.txt'

#config of prices and volumes
config = {
    'price_range': (25000, 35000),
    'volume_range': (1, 100),
    'start_date': datetime(2023, 1, 1),
    'end_date': datetime(2023, 1, 5),
    'frequency': '1H'
}

#fee in persentages
TRANSACTION_FEE = 0.01

# Maximum available amout for one operation
MAX_TRANSACTION_VOL = 500