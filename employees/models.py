from django.db import models


class Department(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Employee(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    employee_id = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=15)
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department  = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    designation = models.CharField(max_length=100)
    salary      = models.DecimalField(max_digits=10, decimal_places=2)
    join_date   = models.DateField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    photo       = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

    class Meta:
        ordering = ['employee_id']


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('half_day', 'Half Day'),
        ('leave',   'Leave'),
    ]

    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date       = models.DateField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in   = models.TimeField(blank=True, null=True)
    check_out  = models.TimeField(blank=True, null=True)
    remarks    = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
