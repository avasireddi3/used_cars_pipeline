INSERT INTO test_listings
SELECT ls.id,ls.variant_id,ls.body_type,
    ls.city,ls.price,ls.fuel_type,ls.mileage,
    ls.make,ls.model,ls.gear,ls.owner
FROM listings_staging as ls
LEFT JOIN test_listings as tl ON ls.id = tl.id
WHERE tl.id IS NULL