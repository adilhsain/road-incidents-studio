# Road Incidents — Investigating Road Safety in Victoria\n\n### Project Overview
This project explores road safety in Victoria by analyzing accident, person and vehicle data to inform safer transport practices. It is designed as a student web application to present insights into injury outcomes, risk groups, and data-driven road safety decisions.

### Team
| Name | Student Number | Role |
|------|----------------|------|
| Student A Name | s1234567 | Student A |
| Your Name Here | s7654321 | Student B |

### Tech Stack
- Backend: Python 3.x + Flask
- Database: MySQL
- Frontend: HTML5, CSS3, Vanilla JavaScript

### Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MySQL database:
   ```bash
   mysql -u <username> -p < database/schema.sql
   mysql -u <username> -p < database/seed_data.sql
   ```
4. Configure DB credentials in `app/db.py`
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

