from datetime import timedelta

from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(
    style="{",
    format="[{asctime}] [{levelname}] {message}",
    datefmt="%B %d, %G %H:%M:%S"
)
log = logging.getLogger("MindustryServerStats")
log.setLevel(logging.INFO)

UPDATER_DELAY = 5
MAX_DELAY = timedelta(seconds=10)
