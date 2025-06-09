class Servers:
    id: int
    ip: str
    port: int

    def __init__(self, row_id: int, ip: str, port: int):
        self.id = row_id
        self.ip = ip
        self.port = port
