import os
import threading
import time
from datetime import datetime
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

from pydustry import Server as MindustryServer

from mindustry_server_stats.database.database import Database
from mindustry_server_stats.database.popos import server_name, server_description, datapoint
from mindustry_server_stats.database.popos.server import Server
from mindustry_server_stats.globals import log

ROOT_DIRECTORY = Path(os.path.realpath(__file__)).parent.parent
DATA_FILE = Path("")

def update_once(server: Server):
    # Not taking this as an argument as cross-thread accesses are not allowed.
    database = Database()

    try:
        server_status = MindustryServer(server.ip, server.port).get_status()
    except TimeoutError:
        log.warn(f"Timeout on {server.ip}:{server.port} (id: {server.id})")
        return
    except OSError as e:
        log.warn(f"OSError on {server.ip}:{server.port} (id: {server.id})")
        log.warn(e.with_traceback(None))
        return

    name_datapoint = server_name.ServerName(None, server.id, server_status.name)
    description_datapoint = server_description.ServerDescription(None, server.id, server_status.desc)

    database.insert_name(name_datapoint)
    database.insert_description(description_datapoint)

    name_index = database.get_names(server.id)[-1].id
    description_index = database.get_descriptions(server.id)[-1].id

    current_time = datetime.now()
    server_datapoint = datapoint.Datapoint(None, server.id, current_time.timestamp(), name_index,
                                           description_index, server_status.players, server_status.ping,
                                           server_status.wave)
    database.insert_datapoint(server_datapoint)

def periodic_update(duration: int):
    database = Database()
    pool = Pool()

    while True:
        # While this could be outside the loop, doing this can make getting the servers dynamic.
        # Also, it isn't like you're loading hundreds of thousands of entries. *Unlike a certain feature.*
        servers = database.get_servers()
        pool.map(update_once, servers)
        time.sleep(duration)


def run_daemon(delay: int):
    daemon = threading.Thread(target=periodic_update, args=[delay], daemon=True)
    daemon.start()
