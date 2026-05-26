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
