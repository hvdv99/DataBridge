SELECT account_id_hashed, count(*) as total_packages_ordered
FROM delivery_facts
GROUP BY account_id_hashed
ORDER by total_packages_ordered DESC
LIMIT 100;