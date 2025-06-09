import os
import sqlite3
from pathlib import Path
from typing import TypeVar, Type

from mindustry_server_stats.database.popos import datapoint, server, server_name, server_description
from mindustry_server_stats.database.popos.datapoint import Datapoint

DIRECTORY = Path(os.path.realpath(__file__)).parent
DATA_FILE = Path(f"{DIRECTORY}/data.sqlite")
SCHEMA = Path(f"{DIRECTORY}/schema.sql")

DATA_FILE.touch(exist_ok=True)

T = TypeVar('T')

class Database:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.connection = sqlite3.connect(DATA_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.executescript(SCHEMA.read_text())
        self.connection.commit()

    def where_into(self, table: str, cls: T, condition: str, parameters: tuple = tuple()) -> T:
        result = self.cursor.execute(f"SELECT * FROM {table} WHERE {condition}", parameters)
        return cls(*result.fetchone())

    def where_all_into(self, table: str, cls: T, condition: str) -> list[T]:
        objects: list[T] = []
        result = self.cursor.execute(f"SELECT * FROM {table} WHERE {condition}")

        entry: tuple
        for entry in result.fetchall():
            obj = cls(*entry)
            objects.append(obj)

        return objects

    def fetch_all_into(self, table: str, cls: T) -> list[T]:
        return self.where_all_into(table, cls, "id == id")

    def get_last_index(self, table: str) -> int:
        result = self.cursor.execute(f"SELECT seq FROM sqlite_sequence WHERE name == {table}")
        return int(result.fetchone())

    def get_datapoints(self) -> list[Type[Datapoint]]:
        return self.fetch_all_into("datapoints", datapoint.Datapoint)

    def get_datapoint(self, server_hostname: str):
        return self.where_into('datapoints', datapoint.Datapoint,
                               f"datapoints.server_id == ?", (server_hostname,))

    def get_server_datapoints(self, server_id: str, start_at: int) -> list[datapoint.Datapoint]:
        datapoints: list[datapoint.Datapoint] = []
        query = (f"SELECT "
                 f"datapoints.id, server_id, creation_time, name_id, description_id, players, latency, wave "
                 f"FROM datapoints "
                 f"INNER JOIN servers "
                 f"ON servers.id = datapoints.server_id "
                 f"WHERE servers.id = ? "
                 f"AND ? <= creation_time;")
        result = self.cursor.execute(query, [server_id, start_at])

        for entry in result.fetchall():
            datapoints.append(datapoint.Datapoint(*entry))

        return datapoints

    def insert_datapoint(self, obj: datapoint.Datapoint):
        self.cursor.execute(f"INSERT INTO datapoints(server_id, creation_time, name_id, description_id, players, "
                            f"latency, wave) "
                            f"VALUES (?, ?, ?, ?, ?, ?, ?)", (obj.server_id, obj.creation_time, obj.name_id,
                                                              obj.description_id, obj.players, obj.latency, obj.wave))
        self.connection.commit()
        # self.insert('datapoints', (obj.id, obj.server_id, obj.creation_time, obj.name_id,
        #                            obj.description_id, obj.players, obj.latency, obj.wave))

    def get_servers(self) -> list[Type[server.Server]]:
        return self.fetch_all_into("servers", server.Server)

    def get_server(self, server_id: str) -> Type[server.Server]:
        return self.where_into("servers", server.Server, "id == ?", (server_id,))

    def insert_server(self, obj: server.Server):
        self.cursor.execute(f"INSERT INTO servers(ip, port) VALUES (?, ?)", (obj.ip, obj.port))
        self.connection.commit()

    def get_name(self, name_id: int):
        return self.where_into('server_names', server_name.ServerName, f'id == ?', (name_id,))

    def get_names(self, server_id: int):
        return self.where_all_into('server_names', server_name.ServerName, f'server_id == {server_id}')

    def insert_name(self, obj: server_name.ServerName):
        self.cursor.execute(f"INSERT INTO server_names(server_id, name) VALUES (?, ?)",
                            (obj.server_id, obj.data))
        self.connection.commit()

    def get_description(self, description_id: int):
        return self.where_into('server_descriptions', server_name.ServerName, f'id == ?', (description_id,))

    def get_descriptions(self, server_id: int):
        return self.where_all_into('server_descriptions', server_description.ServerDescription,
                                   f'server_id == {server_id}')

    def insert_description(self, obj: server_description.ServerDescription):
        self.cursor.execute(f"INSERT INTO server_descriptions(server_id, description) VALUES (?, ?)",
                            (obj.server_id, obj.data))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


# conn = Database()
#
# server_obj = server.Server(None, "127.0.0.1", 2000)
# name_obj = server_name.ServerName(10, 5, "local")
# description_obj = server_description.ServerDescription(0, 0, "lorem ipsum dolor sit amet")
#
# d_point = datapoint.Datapoint(0, 0, None, 0, 0, 2, 100, 1)
#
# conn.insert_server(server_obj)
#
# for serv in conn.get_servers():
#     print(f"[{serv.id}] {serv.ip}:{serv.port}")
