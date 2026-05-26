-- Level 2B query: summarise people by road user type and injury level,
-- including counts of hospital admissions and ejections.
SELECT
    COALESCE(p.ROAD_USER_TYPE, 'Unknown') AS ROAD_USER_TYPE,
    COALESCE(p.INJ_LEVEL, 'Unknown') AS INJ_LEVEL,
    COUNT(*) AS total_people,
    SUM(CASE WHEN COALESCE(p.TAKEN_HOSPITAL, 'No') = 'Yes' THEN 1 ELSE 0 END) AS hospital_count,
    SUM(CASE WHEN COALESCE(p.EJECTED_CODE, 'Not ejected') != 'Not ejected' THEN 1 ELSE 0 END) AS ejected_count
FROM PERSON p
JOIN ACCIDENT a ON p.ACCIDENT_NO = a.ACCIDENT_NO
WHERE (%s IS NULL OR p.INJ_LEVEL = %s)
GROUP BY ROAD_USER_TYPE, INJ_LEVEL
ORDER BY total_people DESC;

