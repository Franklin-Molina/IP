CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url VARCHAR NOT NULL,
    short_code VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL
);

CREATE TABLE visits (
    id SERIAL PRIMARY KEY,
    url_id INTEGER,
    ip_address VARCHAR,
    user_agent VARCHAR(512),
    referrer VARCHAR(512),
    network_info TEXT,
    cookies TEXT,
    extra_params TEXT,
    device_info VARCHAR(256),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    isp VARCHAR(256),
    timestamp TIMESTAMP,
    FOREIGN KEY (url_id) REFERENCES urls(id)
);
