-- Seed data statements for personas, team members, facts

-- team_members seed data
INSERT INTO team_members (full_name, student_number, role)
VALUES
    ('Tayyab', 's4226244', 'Student B');

-- personas seed data
INSERT INTO personas (name, age, occupation, background, goals, pain_points, assigned_student, image_url)
VALUES
    ('Maya Thompson', 38, 'Local Council Road Safety Officer', 'Works for a local council in Victoria and is responsible for improving road safety within her municipality. She reviews road incident data, identifies high-risk areas, and supports decisions on road maintenance, signage, street lighting, and community safety programs.', 'Identify environmental conditions linked to higher crash rates; improve road safety planning and infrastructure decisions; support funding requests using crash data evidence; reduce crashes in high-risk areas; quickly compare crash patterns across different conditions.', 'Needs easy access to summarised crash information; wants filtering by weather, road surface and lighting conditions; needs visual charts and comparisons that are easy to understand; wants fast access to important crash trends without manually analysing raw data; needs clear insights to support road safety decision making.', 'A', NULL),
    ('Dr Sarah Chen', 45, 'Trauma Research Analyst', 'Trauma research analyst specialising in road incident psychology. She studies how crashes affect cognitive functioning, stress responses, and long-term recovery, using data to develop evidence-based strategies that improve road safety interventions.', 'Use data to identify high-risk patterns and accident conditions such as weather or lighting that lead to severe injuries; analyse safety features such as airbags and seatbelts in Victorian crashes; improve post-crash care by providing emergency services data on which collisions require more attention.', 'Data is often too messy; accident and injury outcomes are not clearly aligned; critical medical information and road logs are kept separately; near misses are not captured, making it harder to identify close calls.', 'B', NULL);

-- facts seed data
INSERT INTO facts (fact_title, fact_value, fact_description, source_page)
VALUES
    ('Road Fatalities in Victoria', '291', 'Number of road fatalities recorded in Victoria in recent years', 'landing'),
    ('Hospital Admissions', '~18,000', 'Estimated serious injury hospitalisations from road crashes per year in Victoria', 'landing'),
    ('Most Vulnerable Road Users', 'Pedestrians & Cyclists', 'Pedestrians and cyclists account for a disproportionate share of serious injuries relative to their road usage', 'landing'),
    ('Seat Belt Compliance', '98.5%', 'Seat belt wearing rate in Victoria, yet unrestrained occupants account for a higher share of fatalities', 'landing');

-- Sample accident and person seed data for summary and deep analyses
INSERT INTO ACCIDENT (ACCIDENT_NO, ACCIDENTDATE, ACCIDENTTIME, ACCIDENT_TYPE, SEVERITY, SPEED_ZONE, NODE_ID, LIGHT_CONDITION, ROAD_SURFACE_TYPE, ATMOSPH_COND, ROAD_GEOMETRY)
VALUES
    (1001, '2025-07-12', '14:35', 'Intersection', 'Serious', 60, 101, 'Daylight', 'Dry', 'Fine', 'Curve'),
    (1002, '2025-08-03', '18:10', 'Urban', 'Serious', 50, 102, 'Dusk', 'Wet', 'Rain', 'Straight'),
    (1003, '2025-08-20', '22:40', 'Freeway', 'Fatal', 100, 103, 'Night', 'Wet', 'Fog', 'Straight'),
    (1004, '2025-09-05', '08:15', 'Urban', 'Minor', 40, 104, 'Daylight', 'Dry', 'Fine', 'Straight');

INSERT INTO PERSON (PERSON_ID, ACCIDENT_NO, SEX, AGE_GROUP, SEATING_POSITION, ROAD_USER_TYPE, HELMET_BELT_WORN, EJECTED_CODE, TAKEN_HOSPITAL, PROT_FACTOR, INJ_LEVEL, LICENCE_STATE)
VALUES
    (1, 1001, 'Male', '26-39', 'Driver', 'Driver', 'Yes', 'Not ejected', 'No', 'Seatbelt', 'Serious Injury', 'VIC'),
    (2, 1001, 'Female', '26-39', 'Passenger', 'Passenger', 'Yes', 'Not ejected', 'No', 'Seatbelt', 'Not Injured', 'VIC'),
    (3, 1002, 'Male', '18-25', 'Driver', 'Motorcyclist', 'No', 'Ejected', 'Yes', 'Helmet', 'Fatal', 'VIC'),
    (4, 1002, 'Female', '18-25', 'Passenger', 'Passenger', 'No', 'Not ejected', 'Yes', 'Seatbelt', 'Other Injury', 'VIC'),
    (5, 1003, 'Male', '65+', 'Driver', 'Driver', 'Yes', 'Not ejected', 'Yes', 'Seatbelt', 'Fatal', 'VIC'),
    (6, 1004, 'Male', '40-64', 'Cyclist', 'Cyclist', 'No', 'Not ejected', 'Yes', 'Helmet', 'Serious Injury', 'VIC'),
    (7, 1004, 'Female', '40-64', 'Driver', 'Driver', 'Yes', 'Not ejected', 'No', 'Seatbelt', 'Not Injured', 'VIC'),
    (8, 1004, 'Female', '13-17', 'Passenger', 'Passenger', 'Yes', 'Not ejected', 'No', 'Seatbelt', 'Other Injury', 'VIC');
