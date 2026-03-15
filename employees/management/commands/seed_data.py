"""
Management command: seed_data
Location: employees/management/commands/seed_data.py

Run with: python manage.py seed_data
"""
import sys, os
# Add the project root to sys.path so employees app is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Department, Employee, Attendance
import datetime, random


class Command(BaseCommand):
    help = 'Seeds the database with sample departments, employees, and attendance records.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database...'))

        # ── Create Superuser ────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin123', email='admin@ems.com')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists, skipping.'))

        # ── Create Departments ──────────────────────────────────────────
        dept_data = [
            ('Engineering',     'Software development and tech infrastructure'),
            ('Human Resources', 'Recruitment, payroll, and employee welfare'),
            ('Finance',         'Accounts, budgeting and financial reporting'),
            ('Marketing',       'Brand management, campaigns and growth'),
            ('Operations',      'Day-to-day business operations management'),
            ('Sales',           'Client acquisition and revenue generation'),
        ]
        departments = {}
        for name, desc in dept_data:
            dept, created = Department.objects.get_or_create(name=name, defaults={'description': desc})
            departments[name] = dept
            status = 'created' if created else 'already exists'
            self.stdout.write(f'  Department "{name}" - {status}')

        # ── Create Employees ────────────────────────────────────────────
        employees_data = [
            ('EMP001', 'Arjun Sharma',      'arjun@ems.com',    '+91-9876543210', 'M', 'Engineering',     'Senior Developer',    85000, '2022-01-15', 'active'),
            ('EMP002', 'Priya Patel',       'priya@ems.com',    '+91-9876543211', 'F', 'Human Resources', 'HR Manager',          72000, '2021-06-01', 'active'),
            ('EMP003', 'Rohit Verma',       'rohit@ems.com',    '+91-9876543212', 'M', 'Finance',         'Finance Analyst',     68000, '2022-03-20', 'active'),
            ('EMP004', 'Sneha Iyer',        'sneha@ems.com',    '+91-9876543213', 'F', 'Marketing',       'Marketing Lead',      75000, '2021-11-10', 'active'),
            ('EMP005', 'Vikram Singh',      'vikram@ems.com',   '+91-9876543214', 'M', 'Sales',           'Sales Manager',       90000, '2020-08-05', 'active'),
            ('EMP006', 'Kavya Reddy',       'kavya@ems.com',    '+91-9876543215', 'F', 'Engineering',     'Backend Engineer',    78000, '2023-01-02', 'active'),
            ('EMP007', 'Amit Joshi',        'amit@ems.com',     '+91-9876543216', 'M', 'Operations',      'Operations Manager',  80000, '2021-04-15', 'active'),
            ('EMP008', 'Deepika Nair',      'deepika@ems.com',  '+91-9876543217', 'F', 'Finance',         'Senior Accountant',   65000, '2022-07-18', 'active'),
            ('EMP009', 'Rahul Mehta',       'rahul@ems.com',    '+91-9876543218', 'M', 'Engineering',     'DevOps Engineer',     82000, '2023-03-01', 'active'),
            ('EMP010', 'Ananya Gupta',      'ananya@ems.com',   '+91-9876543219', 'F', 'Marketing',       'Content Strategist',  60000, '2022-09-12', 'active'),
            ('EMP011', 'Kiran Bose',        'kiran@ems.com',    '+91-9876543220', 'M', 'Sales',           'Sales Executive',     55000, '2023-05-20', 'active'),
            ('EMP012', 'Meera Kapoor',      'meera@ems.com',    '+91-9876543221', 'F', 'Human Resources', 'HR Executive',        50000, '2023-02-14', 'active'),
            ('EMP013', 'Suresh Kumar',      'suresh@ems.com',   '+91-9876543222', 'M', 'Engineering',     'Frontend Developer',  76000, '2022-11-01', 'active'),
            ('EMP014', 'Farika Khan',       'farika@ems.com',   '+91-9876543223', 'F', 'Operations',      'Operations Analyst',  58000, '2022-06-30', 'inactive'),
            ('EMP015', 'Naveen Pillai',     'naveen@ems.com',   '+91-9876543224', 'M', 'Finance',         'CFO',                 150000, '2019-01-10', 'active'),
        ]

        created_employees = []
        for (emp_id, name, email, phone, gender, dept_name, desig, salary, join_date, status) in employees_data:
            emp, created = Employee.objects.get_or_create(
                employee_id=emp_id,
                defaults={
                    'name':        name,
                    'email':       email,
                    'phone':       phone,
                    'gender':      gender,
                    'department':  departments[dept_name],
                    'designation': desig,
                    'salary':      salary,
                    'join_date':   join_date,
                    'status':      status,
                }
            )
            created_employees.append(emp)
            flag = '(new)' if created else '(exists)'
            self.stdout.write(f'  Employee {emp_id} - {name} {flag}')

        # ── Create Attendance for last 7 days ───────────────────────────
        attendance_statuses = ['present', 'present', 'present', 'present', 'absent', 'half_day', 'leave']
        today = datetime.date.today()
        count = 0
        for emp in created_employees:
            for delta in range(7):
                day = today - datetime.timedelta(days=delta)
                # Skip weekends
                if day.weekday() >= 5:
                    continue
                status = random.choice(attendance_statuses)
                check_in  = datetime.time(9, random.randint(0, 30))  if status in ('present', 'half_day') else None
                check_out = datetime.time(17, random.randint(0, 59)) if status == 'present' else None
                Attendance.objects.get_or_create(
                    employee=emp,
                    date=day,
                    defaults={
                        'status':    status,
                        'check_in':  check_in,
                        'check_out': check_out,
                        'remarks':   '',
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'\nSeeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'   Departments : {len(dept_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   Employees   : {len(employees_data)}'))
        self.stdout.write(self.style.SUCCESS(f'   Attendance  : {count} records'))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        self.stdout.write(self.style.WARNING('  Admin Panel  : http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.WARNING('  Username     : admin'))
        self.stdout.write(self.style.WARNING('  Password     : admin123'))
        self.stdout.write(self.style.WARNING('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
