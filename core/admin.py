from django.contrib import admin
from .models import Expense, Attendence, Staff, IncomeStatement, Appointments, Workflow

# Register your models here.

admin.site.register(Expense)
admin.site.register(Attendence)
admin.site.register(Staff)
admin.site.register(IncomeStatement)
admin.site.register(Appointments)
admin.site.register(Workflow)