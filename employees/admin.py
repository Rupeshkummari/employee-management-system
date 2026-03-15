from django.contrib import admin
from .models import Employee, Department, Attendance


# ── Department Admin ────────────────────────────────────────────────────────

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display   = ('name', 'description', 'employee_count', 'created_at')
    search_fields  = ('name',)
    ordering       = ('name',)

    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'


# ── Employee Admin ──────────────────────────────────────────────────────────

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display   = ('employee_id', 'name', 'email', 'phone', 'department', 'designation', 'salary', 'status', 'join_date')
    search_fields  = ('employee_id', 'name', 'email', 'phone')
    list_filter    = ('status', 'department', 'gender')
    list_per_page  = 20
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('employee_id', 'name', 'email', 'phone', 'gender', 'photo')
        }),
        ('Employment Details', {
            'fields': ('department', 'designation', 'salary', 'join_date', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ── Attendance Admin ────────────────────────────────────────────────────────

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display   = ('employee', 'date', 'status', 'check_in', 'check_out', 'remarks')
    list_filter    = ('status', 'date', 'employee__department')
    search_fields  = ('employee__name', 'employee__employee_id')
    list_per_page  = 25
    date_hierarchy = 'date'
