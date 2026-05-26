-- Query to retrieve all personas and team members for the mission page
SELECT * FROM personas WHERE assigned_student = 'B';
SELECT * FROM team_members ORDER BY member_id;
SELECT * FROM facts WHERE source_page = 'landing';

