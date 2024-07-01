# logging_config.py
import logging
import os
from datetime import datetime

class LoggingHandler:
    def __init__(self, log_folder='logs'):
        self.log_folder = log_folder
        self.logger = logging.getLogger()
        self.error_handler = self.ErrorHandler()

        self.setup_logging()

    def setup_logging(self):
        os.makedirs(self.log_folder, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = os.path.join(self.log_folder, f'hfc_log_{timestamp}.log')

        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # File handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Stream handler for console output (errors only)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # Add the custom error handler
        self.logger.addHandler(self.error_handler)

    class ErrorHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.error_count = 0

        def emit(self, record):
            if record.levelno >= logging.ERROR:
                self.error_count += 1

    def get_error_count(self):
        return self.error_handler.error_count
