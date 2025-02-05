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