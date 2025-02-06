CREATE TABLE IF NOT EXISTS test_listings
    (id int PRIMARY KEY,
    variant_id int NOT NULL,
    body_type varchar(30),
    city varchar(30),
    price int,
    fuel_type varchar(30),
    mileage int,
    make varchar(60),
    model varchar(100),
    gear varchar(30),
    owner varchar(30)
    );

CREATE TABLE IF NOT EXISTS test_new_listings
    (id int PRIMARY KEY,
    variant_id int NOT NULL,
    body_type varchar(30),
    city varchar(30),
    price int,
    fuel_type varchar(30),
    mileage int,
    make varchar(60),
    model varchar(100),
    gear varchar(30),
    owner varchar(30)
    );

CREATE TABLE IF NOT EXISTS test_variants
    (variant_id int PRIMARY KEY,
    engine_cc int,
    ground_clearance_mm int,
    mileage_kmpl int,
    drive_type varchar(30),
    seating_capacity int,
    power int,
    cylinders int,
    gearbox varchar(30),
    top_speed_kmph int,
    enc varchar(30),
    length_mm int,
    width_mm int,
    height_mm int
    );

CREATE TABLE IF NOT EXISTS test_status
    (id int,
    status varchar(10),
    update_time timestamp
    );

TRUNCATE test_new_listings