import datetime

from matplotlib import pyplot as plt
from mindustry_server_stats import data_updater
from mindustry_server_stats.database.database import Database
import numpy as np

data_updater.run_daemon(1)
database = Database()

plt.ion()

def update_figure():
    datapoints = database.get_datapoints()

    time = []
    count = []
    previous_creation_time: datetime.datetime | None = None

    for index, datapoint in enumerate(datapoints):
        creation_time = datetime.datetime.fromisoformat(datapoint.creation_time)
        max_time_delta = datetime.timedelta(seconds=5)

        if (previous_creation_time is not None) and ((creation_time - previous_creation_time) >= max_time_delta):
            time.append(np.datetime64('NaT'))
            count.append(np.nan)

        time.append(creation_time)
        count.append(datapoint.players)
        previous_creation_time = creation_time

    plt.plot(time, count)
    plt.xlim(left=(previous_creation_time - datetime.timedelta(minutes=5)))
    # plt.show(block=False)
    plt.pause(1)
    plt.clf()

while True:
    update_figure()
