import psycopg2

import credentials_test
conn = psycopg2.connect(database= "usedcars2",
                         user = credentials_test.user,
                         host = credentials_test.host,
                         password = credentials_test.password,
                         port = 5432)
cur = conn.cursor()

def initialize_tables()->None:
#create table for used car listings
    cur.execute("""CREATE TABLE IF NOT EXISTS demo1(
                    id INTEGER PRIMARY KEY,
                    variantid INTEGER,
                    bodytype VARCHAR,
                    city VARCHAR,
                    price INTEGER,
                    fueltype VARCHAR,
                    mileage VARCHAR,
                    make VARCHAR,
                    model VARCHAR,
                    gear VARCHAR,
                    owner VARCHAR)
                """)

#create table for car variant information
    cur.execute("""CREATE TABLE IF NOT EXISTS variant_details(
                    variant_id INTEGER PRIMARY KEY,
                    engine_cc INTEGER,
                    ground_clearance_mm INTEGER,
                    mileage_kmpl REAL,
                    drive_type VARCHAR,
                    seating INTEGER,
                    power REAL,
                    cylinders INTEGER,
                    gearbox VARCHAR,
                    top_speed_kmph REAL,
                    enc VARCHAR,
                    length_mm INTEGER,
                    width_mm INTEGER,
                    height_mm INTEGER
                    )
                """)

def check_variant_exists(variant_id:int)->bool:
    #check if variant info already exists in table
    check_variant = cur.execute("""SELECT * 
                                                FROM variant_details
                                                WHERE variant_id = VALUES(%s)""", variant_id)
    if check_variant:
        return True
    else:
        return False

def insert_variant(variant_id:int,variant_info:dict)->None:
    #insert variant info into database
    cur.execute("""INSERT INTO variant_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (variant_id,
                 variant_info['data']['carSpecification']["top"]["engine"]
                 )
                )

def insert_listing(listing_info:list)->None:
    #insert listing into database
    cur.execute("""INSERT INTO demo1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", listing_info)
    conn.commit()