class Datapoint:
    id: int
    server_id: int
    creation_time: int
    name_id: int
    description_id: int
    players: int
    latency: int
    wave: int

    def __init__(self, row_id: int | None, server_id: int, creation_time: float | int, name_id: int,
                 description_id: int, players: int, latency: int, wave: int):
        self.id = row_id
        self.server_id = server_id
        self.creation_time = int(creation_time)
        self.name_id = name_id
        self.description_id = description_id
        self.players = players
        self.latency = latency
        self.wave = wave
