INSERT INTO test_status
SELECT ls.id,'sold' AS status, CURRENT_TIMESTAMP AS update_time
FROM listings_staging as ls
RIGHT JOIN test_listings as tl ON tl.id = ls.id
WHERE ls.id IS NULL