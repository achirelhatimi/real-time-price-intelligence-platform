CREATE TABLE IF NOT EXISTS price_events (
    id          SERIAL PRIMARY KEY,
    product_id  VARCHAR(50)    NOT NULL,
    price       NUMERIC(10,2)  NOT NULL,
    timestamp   TIMESTAMP      NOT NULL,
    ingested_at TIMESTAMP      DEFAULT NOW()
);