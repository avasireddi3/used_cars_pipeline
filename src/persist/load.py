import psycopg2

import credentials_test
conn = psycopg2.connect(database= "usedcars2",
                         user = credentials_test.user,
                         host = credentials_test.host,
                         password = credentials_test.password,
                         port = 5432)


def initialize_tables()->None:
#create table for used car listings
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS listings_demo(
                        id INTEGER PRIMARY KEY,
                        variant_id INTEGER,
                        body_type VARCHAR,
                        city VARCHAR,
                        price INTEGER,
                        fuel_type VARCHAR,
                        mileage VARCHAR,
                        make VARCHAR,
                        model VARCHAR,
                        gear VARCHAR,
                        owner VARCHAR)
                    """)

#create table for car variant information
        cur.execute("""CREATE TABLE IF NOT EXISTS variants_demo(
                        variant_id INTEGER PRIMARY KEY,
                        engine_cc VARCHAR,
                        ground_clearance_mm VARCHAR,
                        mileage_kmpl VARCHAR,
                        drive_type VARCHAR,
                        seating VARCHAR,
                        power VARCHAR,
                        cylinders VARCHAR,
                        gearbox VARCHAR,
                        top_speed_kmph VARCHAR,
                        enc VARCHAR,
                        length_mm VARCHAR,
                        width_mm VARCHAR,
                        height_mm VARCHAR)
                    """)

def check_variant_exists(variant_id:int)->bool:
    #check if variant info already exists in
    with conn.cursor() as cur:
        cur.execute("""SELECT * 
                            FROM variants_demo
                            WHERE variant_id = %s""", [variant_id])
        if not cur.fetchall():
            return False
        else:
            return True

def check_listing_exists(listing_id:int)->bool:
    #check if listing info already exists in table
    with conn.cursor() as cur:
        cur.execute("""SELECT * 
                            FROM listings_demo
                            WHERE id = %s""", [listing_id])
        if not cur.fetchall():
            return False
        else:
            return True

def insert_variant(variant_id:int,variant_info:list)->None:
    #insert variant info into database
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO variants_demo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    variant_info)

def insert_listing(listing_info:list)->None:
    #insert listing into database
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO listings_demo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", listing_info)
        conn.commit()