from datetime import datetime, timedelta
from mindustry_server_stats.database.database import Database
from mindustry_server_stats.database.popos.datapoint import Datapoint
from mindustry_server_stats.database.popos.server import Server


def server_exists(database:Database, server_id: str) -> bool:
    query = database.cursor.execute("SELECT * FROM servers WHERE id = ?", [server_id])
    return query.fetchone() is not None


def get_server_display(server: Server) -> str:
    return f"{server.ip}:{server.port}" if server.display_name is None else server.display_name


def get_data(server_id: str, minimum_limit: datetime, max_time_delta: timedelta) -> list:
    database: Database = Database()
    datapoints = database.get_server_datapoints(server_id, int(minimum_limit.timestamp()))

    time: list[str | None] = []
    count: list[int | None] = []
    latency: list[int | None] = []
    wave: list[int | None] = []

    # This works because Python does a shallow copy for these lists.
    fields = [time, count, latency, wave]
    previous_creation_time = datetime.fromtimestamp(datapoints[0].creation_time)

    datapoint: Datapoint
    for datapoint in datapoints:
        creation_time = datetime.fromtimestamp(datapoint.creation_time)

        if (creation_time - previous_creation_time) >= max_time_delta:
            for field in fields: field.append(None)

        time.append(creation_time.isoformat())
        count.append(datapoint.players)
        latency.append(datapoint.latency)
        wave.append(datapoint.wave)

        previous_creation_time = creation_time

    return fields
