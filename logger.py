import logging


class SetupLoger:
    """
    Logging setup class for configuring a logger instance.

    This class provides functionality to set up a logger instance with the desired formatting
    and handlers for logging messages.

    Attributes:
        logger (logging.Logger): The configured logger instance.
    """

    def __init__(self):
        """
        Initialize the SetupLoger instance.

        This constructor sets up the logger by calling the _setup_logger method.
        """
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Configure and return a logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger