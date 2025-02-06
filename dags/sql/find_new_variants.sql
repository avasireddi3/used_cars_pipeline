SELECT listings_staging.variant_id
FROM listings_staging
LEFT JOIN test_variants ON listings_staging.variant_id = test_variants.variant_id
WHERE test_variants.variant_id is NULL