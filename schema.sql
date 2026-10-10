-- transport_collection_db;

CREATE TABLE IF NOT EXISTS drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transport_collections (
    id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL REFERENCES drivers(driver_id) ON DELETE RESTRICT,
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    morning_trips INT NOT NULL CHECK (morning_trips >= 0),
    evening_trips INT NOT NULL CHECK (evening_trips >= 0),
    morning_collection NUMERIC(10,2) NOT NULL CHECK (morning_collection >= 0),
    evening_collection NUMERIC(10,2) NOT NULL CHECK (evening_collection >= 0),
    fuel_expense NUMERIC(10,2) NOT NULL CHECK (fuel_expense >= 0),
    other_expense NUMERIC(10,2) NOT NULL CHECK (other_expense >= 0),
    total_trips INT NOT NULL,
    total_collection NUMERIC(10,2) NOT NULL,
    total_expense NUMERIC(10,2) NOT NULL,
    net_collection NUMERIC(10,2) NOT NULL,
    report_file_path TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_collections_date ON transport_collections(collection_date);
CREATE INDEX IF NOT EXISTS idx_collections_driver ON transport_collections(driver_id);
