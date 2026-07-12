# TransitOps

TransitOps is a comprehensive fleet and transit operations management platform built as a Django collaborative project. It streamlines vehicle tracking, driver allocation, trips dispatch, maintenance tracking, and operational expenses in a unified dashboard.

---

## Technology Stack

- **Backend Framework**: Django 5.x (Python 3.13+)
- **Database**: SQLite (Local development)
- **Frontend Framework**: Bootstrap 5 + Bootstrap Icons (Responsive Dashboard Layout)
- **Design Typography**: Google Fonts (`Inter` & `Outfit`)

---

## Project Directory Structure

```text
TransitOps/
│
├── transitops/             # Project Configuration (settings.py, urls.py, wsgi.py)
├── accounts/               # User administration and authorization
├── dashboard/              # Central operations dashboard
├── vehicles/               # Fleet vehicle registry
├── drivers/                # Driver profiling and roster
├── trips/                  # Dispatch logs and active transit routes
├── maintenance/            # Service schedules and maintenance logs
├── expenses/               # Operations expense ledger
│
├── templates/              # Global templates
│   ├── base.html           # Master layout with Bootstrap 5 Navbar/Sidebar
│   └── registration/       
│       └── login.html      # Styled login credentials page
│
├── static/                 # Static Assets
│   ├── css/                # Custom stylesheets
│   ├── js/                 # Client-side scripts
│   └── images/             # Visual assets
│
├── media/                  # User-uploaded files (omitted from Git)
│
├── manage.py               # Django management utility
└── db.sqlite3              # Local SQLite database (omitted from Git)
```

---

## Setup & Local Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository & Navigate to Project
```bash
git clone https://github.com/AkhilKanswal/TransitOps.git
cd TransitOps
```

### 2. Switch to Your Target Branch
For backend developers:
```bash
git checkout backend
```

### 3. Initialize Virtual Environment
Create and activate a Python virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Install Django 5.x:
```bash
pip install django
```
*(Note: As the project grows, remember to keep your dependencies updated in `requirements.txt` using `pip freeze > requirements.txt`)*.

### 5. Run Database Migrations
Initialize the local database:
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
To access the Django admin console:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
Start the local server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to view the application.

---

## Git Branching & Collaboration Strategy

To maintain a clean and conflict-free release cycle, we follow a feature-branching workflow:

* **`main`**: The stable, production-ready release branch. No direct commits allowed. Code gets merged here only via approved Pull Requests.
* **`backend`**: Integration branch for backend development. All backend feature branches should branch off from `backend` and merge back into `backend` via Pull Requests.
* **`frontend`**: Integration branch for frontend development.
* **Feature Branches**: Format your branches as `feature/<branch-name>` or `bugfix/<issue-name>`. Always branch from the appropriate integration branch (`backend` or `frontend`).

---

## Best Practices

- **Never Commit Secrets**: Do not commit `.env`, api keys, or custom database credentials. Use environment variables.
- **Do Not Ignore Migrations**: Django migration files are vital to synchronize the database schema among team members. Always commit files created under `<app_name>/migrations/`.
- **Maintain PEP 8 Standards**: Write clean Python code with descriptive docstrings.