

CREATE TABLE IF NOT EXISTS drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transport_collections (
    id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL REFERENCES drivers(driver_id) ON DELETE CASCADE,
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


INSERT INTO drivers (driver_name, phone_number, is_active)
VALUES
    ('Arun Kumar', '9876543210', TRUE),
    ('Karthik Raj', '9876543211', TRUE),
    ('Suresh Kumar', '9876543212', TRUE),
    ('Praveen Kumar', '9876543213', FALSE);


INSERT INTO transport_collections (
    driver_id,
    vehicle_number,
    collection_date,
    morning_trips,
    evening_trips,
    morning_collection,
    evening_collection,
    fuel_expense,
    other_expense,
    total_trips,
    total_collection,
    total_expense,
    net_collection
)
VALUES
(
    1, 'TN38AB1234', '2026-10-07',
    5, 4, 2500.00, 2200.00, 900.00, 150.00,
    9, 4700.00, 1050.00, 3650.00
),
(
    2, 'TN38CD5678', '2026-10-07',
    4, 3, 1800.00, 1600.00, 700.00, 100.00,
    7, 3400.00, 800.00, 2600.00
),
(
    3, 'TN37EF9012', '2026-10-08',
    6, 5, 3000.00, 2700.00, 1000.00, 200.00,
    11, 5700.00, 1200.00, 4500.00
),
(	
    1, 'TN38AB1234', '2026-10-08',
    5, 5, 2600.00, 2400.00, 950.00, 120.00,
    10, 5000.00, 1070.00, 3930.00
);

SELECT * FROM transport_collections

DROP TABLE IF EXISTS transport_collections;
DROP TABLE IF EXISTS drivers;

