-- =============================================================
-- Postfix
-- =============================================================
-- alias is used as a Postfix sqlite map.
--
CREATE TABLE IF NOT EXISTS alias (
    alias          TEXT PRIMARY KEY,
    date_created   REAL DEFAULT (datetime('now', 'localtime')),
    forward        TEXT NOT NULL,
    active         INTEGER DEFAULT 1
);

-- =============================================================
-- ${HOME}/Maildir
-- =============================================================
CREATE TABLE IF NOT EXISTS sender (
    sender         TEXT PRIMARY KEY,
    date_created   REAL DEFAULT (datetime('now', 'localtime')),
    date_used      REAL,
    used           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS receiver (
    receiver       TEXT PRIMARY KEY,
    date_created   REAL DEFAULT (datetime('now', 'localtime')),
    date_used      REAL,
    used           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS message (
    message_id     TEXT PRIMARY KEY,
    date_created   REAL DEFAULT (datetime('now', 'localtime')),
    message_date   REAL NOT NULL,
    sender         TEXT NOT NULL,
    receiver       TEXT NOT NULL,
    subject        TEXT NOT NULL,
    FOREIGN KEY (sender) REFERENCES sender(sender),
    FOREIGN KEY (receiver) REFERENCES receiver(receiver)
);

CREATE TABLE IF NOT EXISTS sequence (
    name           TEXT PRIMARY KEY,
    date_created   REAL DEFAULT (datetime('now', 'localtime')),
    date_used      REAL,
    sequence       INTEGER NOT NULL DEFAULT 0
);

INSERT INTO sequence (name, sequence) VALUES('cvdg', 210000);
