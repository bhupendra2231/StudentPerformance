import logging
import os
from datetime import datetime

# Generate a log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the logs directory path
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

# Define the complete log file path
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


