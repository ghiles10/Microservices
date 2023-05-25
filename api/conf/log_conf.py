import os
import sys
from pathlib import Path
import logging

FILE_DIR = Path(__file__).resolve().parents[0]

if not os.path.exists(f"{FILE_DIR.parent}/log/"):
    os.mkdir(f"{FILE_DIR.parent}/log/")

file_name = os.path.basename(sys.argv[0]).split(".")[0]


logger = logging.getLogger(file_name)
handler = logging.FileHandler(f"{FILE_DIR.parent}/log/{file_name}.log", mode="w")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s  - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

