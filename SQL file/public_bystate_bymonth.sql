
SELECT state, DATE_TRUNC('month', ABNStatusFromDate) AS month, COUNT(*) as total
FROM my_db.active_public_company
GROUP BY state, month
ORDER BY state, month;
