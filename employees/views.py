from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Department, Attendance
from django.db.models import Sum, Avg
import datetime


# ── Authentication ────────────────────────────────────────────────────

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'employees/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    today = datetime.date.today()
    context = {
        'total_employees':    Employee.objects.count(),
        'active_employees':   Employee.objects.filter(status='active').count(),
        'total_departments':  Department.objects.count(),
        'present_today':      Attendance.objects.filter(date=today, status='present').count(),
        'recent_employees':   Employee.objects.order_by('-created_at')[:5],
        'departments':        Department.objects.all(),
    }
    return render(request, 'employees/dashboard.html', context)


# ── Employee CRUD ─────────────────────────────────────────────────────

@login_required
def employee_list(request):
    query      = request.GET.get('q', '')
    department = request.GET.get('department', '')
    employees  = Employee.objects.select_related('department').all()
    if query:
        employees = employees.filter(name__icontains=query)
    if department:
        employees = employees.filter(department__id=department)
    departments = Department.objects.all()
    return render(request, 'employees/employee_list.html', {
        'employees': employees, 'query': query, 'departments': departments
    })


@login_required
def employee_detail(request, pk):
    employee   = get_object_or_404(Employee, pk=pk)
    attendance = Attendance.objects.filter(employee=employee).order_by('-date')[:30]
    return render(request, 'employees/employee_detail.html', {
        'employee': employee, 'attendance': attendance
    })


@login_required
def employee_add(request):
    if request.method == 'POST':
        Employee.objects.create(
            employee_id = request.POST.get('employee_id'),
            name        = request.POST.get('name'),
            email       = request.POST.get('email'),
            phone       = request.POST.get('phone'),
            gender      = request.POST.get('gender'),
            department  = get_object_or_404(Department, pk=request.POST.get('department')),
            designation = request.POST.get('designation'),
            salary      = request.POST.get('salary'),
            join_date   = request.POST.get('join_date'),
            status      = request.POST.get('status', 'active'),
            photo       = request.FILES.get('photo'),
        )
        messages.success(request, 'Employee added successfully.')
        return redirect('employee_list')
    departments = Department.objects.all()
    return render(request, 'employees/employee_form.html', {
        'action': 'Add', 'departments': departments
    })


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.employee_id = request.POST.get('employee_id')
        employee.name        = request.POST.get('name')
        employee.email       = request.POST.get('email')
        employee.phone       = request.POST.get('phone')
        employee.gender      = request.POST.get('gender')
        employee.department  = get_object_or_404(Department, pk=request.POST.get('department'))
        employee.designation = request.POST.get('designation')
        employee.salary      = request.POST.get('salary')
        employee.join_date   = request.POST.get('join_date')
        employee.status      = request.POST.get('status', 'active')
        if request.FILES.get('photo'):
            employee.photo = request.FILES.get('photo')
        employee.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('employee_list')
    departments = Department.objects.all()
    return render(request, 'employees/employee_form.html', {
        'action': 'Edit', 'employee': employee, 'departments': departments
    })


@login_required
def employee_delete(request, pk):
    get_object_or_404(Employee, pk=pk).delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list')


# ── Department CRUD ───────────────────────────────────────────────────

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
def department_add(request):
    if request.method == 'POST':
        Department.objects.create(
            name        = request.POST.get('name'),
            description = request.POST.get('description', ''),
        )
        messages.success(request, 'Department added successfully.')
        return redirect('department_list')
    return render(request, 'employees/department_form.html', {'action': 'Add'})


@login_required
def department_delete(request, pk):
    get_object_or_404(Department, pk=pk).delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('department_list')


# ── Salary / Payroll ──────────────────────────────────────────

@login_required
def salary_list(request):
    employees = Employee.objects.select_related('department').all()
    total_payroll = employees.aggregate(total=Sum('salary'))['total'] or 0
    avg_salary    = employees.aggregate(avg=Avg('salary'))['avg'] or 0
    return render(request, 'employees/salary_list.html', {
        'employees':    employees,
        'total_payroll': total_payroll,
        'avg_salary':    avg_salary,
    })


# ── Leave Management ──────────────────────────────────────────

@login_required
def leave_list(request):
    employees_list = Employee.objects.filter(status='active')
    # Placeholder: no Leave model yet — pass empty list
    leaves = []
    return render(request, 'employees/leave_list.html', {
        'leaves':         leaves,
        'employees_list': employees_list,
    })


# ── Attendance ────────────────────────────────────────────────────────

@login_required
def attendance_list(request):
    date       = request.GET.get('date', str(datetime.date.today()))
    attendance = Attendance.objects.filter(date=date).select_related('employee')
    return render(request, 'employees/attendance_list.html', {
        'attendance': attendance, 'date': date
    })


@login_required
def attendance_mark(request):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=request.POST.get('employee'))
        date     = request.POST.get('date')
        obj, created = Attendance.objects.update_or_create(
            employee=employee, date=date,
            defaults={
                'status':    request.POST.get('status', 'present'),
                'check_in':  request.POST.get('check_in') or None,
                'check_out': request.POST.get('check_out') or None,
                'remarks':   request.POST.get('remarks', ''),
            }
        )
        messages.success(request, 'Attendance marked successfully.')
        return redirect('attendance_list')
    employees = Employee.objects.filter(status='active')
    return render(request, 'employees/attendance_form.html', {
        'employees': employees,
        'today': str(datetime.date.today())
    })
