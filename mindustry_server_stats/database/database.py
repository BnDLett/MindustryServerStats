import os
import sqlite3
from pathlib import Path

DIRECTORY = Path(os.path.realpath(__file__)).parent
DATA_FILE = Path(f"{DIRECTORY}/data.sqlite")

class Connection:
    pass
