CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE visits (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    ip_address TEXT,
    user_agent VARCHAR(512),
    referrer VARCHAR(512),
    network_info TEXT,
    cookies TEXT,
    extra_params TEXT,
    device_info VARCHAR(256),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    isp VARCHAR(256),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
