from xmlrpc.client import DateTime


class Datapoints:
    id: int
    server_id: int
    creation_time: DateTime
    name_id: int
    description_id: int
    players: int
    latency: int
    wave: int

    def __init__(self, row_id: int, server_id: int, creation_time: DateTime, name_id: int, description_id: int,
                 players: int, latency: int, wave: int):
        self.id = row_id
        self.server_id = server_id
        self.creation_time = creation_time
        self.name_id = name_id
        self.description_id = description_id
        self.players = players
        self.latency = latency
        self.wave = wave
