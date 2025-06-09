class Server:
    id: int
    display_name: str
    ip: str
    port: int

    def __init__(self, row_id: int | None, display_name: str, ip: str, port: int):
        self.id = row_id
        self.display_name = display_name
        self.ip = ip
        self.port = port
