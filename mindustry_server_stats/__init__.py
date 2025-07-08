from mindustry_server_stats import data_updater
from mindustry_server_stats import routes
from mindustry_server_stats.globals import UPDATER_DELAY, app

data_updater.run_daemon(UPDATER_DELAY)
