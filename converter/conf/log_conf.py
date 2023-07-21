import os
from pathlib import Path
import logging

# retrieve the path of the current file
ROOT_DIR = "."

# create a log folder if it does not exist in the parent directory of the current file
if not os.path.exists(f"{ROOT_DIR}/log/"):
    os.mkdir(f"{ROOT_DIR}/log/")



def setup_logger(name_file) : 

    ''' setup a logger object and return it'''


    # create a logger object and set the logging level to INFO 
    logger = logging.getLogger(name_file)
    handler = logging.FileHandler(f"{ROOT_DIR}/log/{name_file}.log", mode="w")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s  - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger 
