CREATE TABLE IF NOT EXISTS servers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name    TEXT,
    ip              TEXT NOT NULL,
    port            INTEGER NOT NULL,

    UNIQUE(ip, port) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS server_names (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id   INTEGER REFERENCES id,
    name        TEXT NOT NULL,

    UNIQUE(server_id, name) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS server_descriptions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id       INTEGER REFERENCES id,
    description     TEXT NOT NULL,

    UNIQUE(server_id, description) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS datapoints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id       INTEGER NOT NULL REFERENCES servers(id),
    -- Admittedly overkill, but it gets the job done.
    creation_time   INT NOT NULL,
    name_id         INTEGER REFERENCES server_names(id),
    description_id  INTEGER REFERENCES server_descriptions(id),
    players         INTEGER NOT NULL,
    latency         INTEGER NOT NULL,
    wave            INTEGER NOT NULL
);
