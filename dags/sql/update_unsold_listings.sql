INSERT INTO test_status
SELECT nl.id AS id,'unsold' AS status, CURRENT_TIMESTAMP AS update_time
FROM test_new_listings AS nl