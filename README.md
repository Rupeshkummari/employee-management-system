# Employee Management System

A full-stack web application to manage employee profiles, department assignments, and attendance records — built with Django and Python.

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML5, CSS3, Bootstrap, JavaScript  |
| Backend   | Python 3.12, Django 5.1             |
| Database  | SQLite3 (easily switchable to MySQL)|
| Auth      | Django built-in authentication      |
| Tools     | Postman, Git, VS Code               |

## Features

- Admin login with protected dashboard
- Employee CRUD — Add, view, edit, delete employee records
- Employee photo upload and profile display
- Department management — Add and manage departments
- Attendance tracking — Mark daily attendance (Present, Absent, Half Day, Leave)
- Check-in and check-out time recording
- Filter employees by department or search by name
- Dashboard with real-time stats — total employees, present today, department count
- Django Admin panel for backend management

## Database Schema

```
Department      Employee              Attendance
----------      --------              ----------
id              id                    id
name            employee_id           employee (FK)
description     name                  date
                email                 status
                phone                 check_in
                gender                check_out
                department (FK)       remarks
                designation
                salary
                join_date
                status
                photo
```

## Project Structure

```
employee-management-system/
├── core/
│   ├── manage.py
│   └── core/
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│       └── asgi.py
├── employees/
│   ├── models.py        # Employee, Department, Attendance models
│   ├── views.py         # All CRUD and auth views
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin panel config
│   └── templates/
│       └── employees/   # HTML templates
├── templates/
│   └── static/
│       ├── css/
│       └── js/
├── requirements.txt
└── .gitignore
```

## Setup and Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Rupeshkummari/employee-management-system.git
cd employee-management-system/core

# 2. Create and activate virtual environment
python -m venv env
env\Scripts\activate        # Windows
source env/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r ../requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Developer

**Rupesh K**
- GitHub: [github.com/Rupeshkummari](https://github.com/Rupeshkummari)
- LinkedIn: [linkedin.com/in/kummari-rupesh-76325a251](https://linkedin.com/in/kummari-rupesh-76325a251)
- Email: rupeshkummari223@gmail.com
