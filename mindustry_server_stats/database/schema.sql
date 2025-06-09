CREATE TABLE IF NOT EXISTS servers (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ip      TEXT NOT NULL,
    port    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER REFERENCES id,
    name TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER REFERENCES id,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS datapoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL REFERENCES servers(id),
    creation_time TEXT NOT NULL DEFAULT current_timestamp,
    name TEXT REFERENCES descriptions(description),
    players INTEGER NOT NULL,
    latency INTEGER NOT NULL,
    wave INTEGER NOT NULL,
);
