CREATE TABLE locations
(
    id        SERIAL PRIMARY KEY,
    device_id VARCHAR(255) NOT NULL,
    latitude  FLOAT        NOT NULL,
    longitude FLOAT        NOT NULL,
    speed     FLOAT        NOT NULL,
    timestamp TIMESTAMP    NOT NULL
);