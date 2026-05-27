-- Seed data statements for personas, team members, facts

-- team_members seed data
INSERT INTO team_members (full_name, student_number, role)
VALUES
    ('Student A Name', 's1234567', 'Student A'),
    ('Your Name Here', 's7654321', 'Student B');

-- personas seed data
INSERT INTO personas (name, age, occupation, background, goals, pain_points, assigned_student, image_url)
VALUES
    ('Marcus Chen', 45, 'Road Safety Policy Analyst',
     'Works at the Department of Transport, analyses road condition data to recommend infrastructure improvements.',
     'Identify which atmospheric and road surface conditions correlate with highest accident severity. Compare accident rates across different speed zones and light conditions.',
     'Data is scattered across multiple reports, hard to visualise trends, time-consuming to find meaningful patterns.',
     'A',
     NULL),
    ('Dr. Sarah Mitchell', 38, 'Emergency Medicine Researcher',
     'Conducts research at Royal Melbourne Hospital studying injury patterns from road accidents to improve emergency response protocols.',
     'Understand which types of road users suffer the most severe injuries, identify patterns in hospital admission rates, determine if age group or seating position affects injury severity.',
     'Needs aggregated injury data quickly, current reports do not link ejection data with injury outcomes, difficult to identify at-risk demographic groups.',
     'B',
     NULL);

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
