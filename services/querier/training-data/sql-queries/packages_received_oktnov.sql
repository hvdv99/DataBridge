SELECT COUNT(DISTINCT cp.id) AS total_packages_received
FROM collo_packages cp
JOIN delivery_preference dp ON cp.account_id_hashed = dp.account_id_hashed
WHERE cp.da_datum_acceptatie BETWEEN '2023-10-01' AND '2023-11-30'