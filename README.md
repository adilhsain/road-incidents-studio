# Road Incidents — Investigating Road Safety in Victoria\n\n### Project Overview
This project explores road safety in Victoria by analyzing accident, person and vehicle data to inform safer transport practices. It is designed as a student web application to present insights into injury outcomes, risk groups, and data-driven road safety decisions.

### Team
| Name | Student Number | Role |
|------|----------------|------|
| Student A Name | s1234567 | Student A |
| Your Name Here | s7654321 | Student B |

### Tech Stack
- Backend: Python 3.x + Flask
- Database: SQLite
- Frontend: HTML5, CSS3, Vanilla JavaScript

### Setup Instructions
1. Clone the repository.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. The app will automatically initialize and seed the SQLite database on first run.
5. Run the application:
   ```bash
   python app/app.py
   ```
6. Open `http://localhost:5000`

### Project Structure
```
road-incidents-studio/
├── app/
│   ├── app.py
│   ├── db.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── deep_people.html
│       ├── mission.html
│       └── people.html
├── database/
│   ├── queries/
│   │   ├── level1_b.sql
│   │   ├── level2_b.sql
│   │   └── level3_b.sql
│   ├── schema.sql
│   └── seed_data.sql
├── project_log/
├── report/
└── README.md
```

### Pages
| Page | Route | Level | Description |
|------|-------|-------|-------------|
| Mission Statement | /mission | Level 1B | Website purpose, personas, team |
| People & Injuries | /people | Level 2B | Summarised injury data with filters |
| Deep Analysis | /deep-analysis | Level 3B | Nested query to find above-average risk groups |

### Database
The project uses a university-provided accident dataset with tables such as:
- `ACCIDENT` — crash incident metadata and context
- `PERSON` — people involved in crashes, including injury severity and role
- `VEHICLE` — vehicles linked to each accident and their attributes
- `NODE` — supporting location or environmental data for accident analysis

### Student B — Sub-Task B Focus
Student B focuses on the "people and injuries" dimension of the road accident dataset. This includes summarising injury outcomes, supporting filtered exploration, and highlighting risk groups with deeper analysis.

Implementation status for Student B:
- Level 1 Mission page is live and connected to the database.
- Level 2 People & Injuries page is fully dynamic with injury, age group, and road user filters.
- Level 3 Deep Analysis page uses a nested SQL query and fallback ranking when the sample dataset has uniform counts.
- The app uses local SQLite for data persistence and seed data is created automatically on first run.

