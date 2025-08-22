import logging
import os
from datetime import datetime

# Remove existing handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create logs directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Create timestamped log file
log_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(log_dir, log_file)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

# Test log
logging.info("logging is working properly")