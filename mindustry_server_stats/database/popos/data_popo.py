from dataclasses import dataclass

@dataclass
class DataPOPO:
    """
    A generic data POPO. This is designed specifically with `id, server_id, data` in mind.
    """
    id: int
    server_id: int
    data: str

    def __init__(self, row_id: int | None, server_id: int, data: str):
        self.id = row_id
        self.server_id = server_id
        self.data = data
