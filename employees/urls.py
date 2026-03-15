from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.dashboard,         name='dashboard'),
    path('login/',                        views.login_view,        name='login'),
    path('logout/',                       views.logout_view,       name='logout'),

    # Employees
    path('employees/',                    views.employee_list,     name='employee_list'),
    path('employees/add/',                views.employee_add,      name='employee_add'),
    path('employees/<int:pk>/',           views.employee_detail,   name='employee_detail'),
    path('employees/<int:pk>/edit/',      views.employee_edit,     name='employee_edit'),
    path('employees/<int:pk>/delete/',    views.employee_delete,   name='employee_delete'),

    # Departments
    path('departments/',                  views.department_list,   name='department_list'),
    path('departments/add/',              views.department_add,    name='department_add'),
    path('departments/<int:pk>/delete/',  views.department_delete, name='department_delete'),

    # Attendance
    path('attendance/',                   views.attendance_list,   name='attendance_list'),
    path('attendance/mark/',              views.attendance_mark,   name='attendance_mark'),

    # Salary & Payroll
    path('salary/',                       views.salary_list,       name='salary_list'),

    # Leave Management
    path('leave/',                        views.leave_list,        name='leave_list'),
]
