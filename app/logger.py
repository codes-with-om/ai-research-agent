import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("ai_research_agent")
logger.setLevel(logging.INFO)

logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)