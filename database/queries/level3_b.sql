-- Level 3B nested query: discover combinations of age group,
-- road user type, and injury level that occur more than the average
-- incident count for all grouped combinations.
--
-- The inner subquery computes the average number of incidents per group
-- for every AGE_GROUP / ROAD_USER_TYPE / INJ_LEVEL combination.
-- The outer query then selects only those combinations whose count
-- exceeds this overall average, showing the highest-risk groups.
SELECT
    p.AGE_GROUP,
    p.ROAD_USER_TYPE,
    p.INJ_LEVEL,
    COUNT(*) AS incident_count
FROM PERSON p
JOIN ACCIDENT a USING (ACCIDENT_NO)
GROUP BY p.AGE_GROUP, p.ROAD_USER_TYPE, p.INJ_LEVEL
HAVING COUNT(*) > (
    SELECT AVG(group_count) FROM (
        SELECT COUNT(*) AS group_count
        FROM PERSON p2
        JOIN ACCIDENT a2 USING (ACCIDENT_NO)
        GROUP BY p2.AGE_GROUP, p2.ROAD_USER_TYPE, p2.INJ_LEVEL
    ) AS avg_table
)
ORDER BY incident_count DESC
LIMIT 20;

