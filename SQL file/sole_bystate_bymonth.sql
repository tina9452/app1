
SELECT state, DATE_TRUNC('month', ABNStatusFromDate) AS month, COUNT(*) as total
FROM my_db.active_sole_trader
GROUP BY state, month
ORDER BY state, month;
