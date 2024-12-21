from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
   path('', views.index, name='index'),
   path('attendance/', views.attendance, name='attendance'),

   path('expenses/', views.expenses_page, name='expenses'),
   path('add-expense/', views.add_expense, name='add_expense'),
   path('edit-expense/<int:pk>/', views.edit_expense, name='edit_expense'),
   path('delete-expense/<int:pk>/', views.delete_expense, name='delete_expense'),

   path('income-statement/', views.income_statement, name='income_statement'),
   path('income-statement/<int:pk>/', views.income_statement_detail, name='income_statement_detail'),
   path('add-statement/', views.add_statement, name='add_statement'),
   path('edit-statement/<int:pk>/', views.edit_statement, name='edit_statement'),
   path('delete-statement/<int:pk>/', views.delete_statement, name='delete_statement'),

   path('appointments/', views.appointments, name='appointments'),
   path('add-appointment/', views.add_appointment, name='add_appointment'),
   path('edit-appointment/<int:pk>/', views.edit_appointment, name='edit_appointment'),
   path('delete-appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),

   path('workflow/', views.workflow, name='workflow'),
   path('workflow/add/', views.add_workflow, name='add_workflow'),
   path('workflow/edit/<int:workflow_id>/', views.edit_workflow, name='edit_workflow'),
   path('workflow/delete/<int:workflow_id>/', views.delete_workflow, name='delete_workflow'),
   path('workflow/get/<int:workflow_id>/', views.get_workflow, name='get_workflow'),
   path('workflow/monthly-report/', views.monthly_report, name='monthly_report'),
   path('workflow/monthly-report/<int:year>/<int:month>/', views.monthly_report, name='monthly_report_date'),
   path('staff/<int:staff_id>/monthly-report/', views.staff_monthly_report, name='staff_monthly_report'),
   path('staff/<int:staff_id>/monthly-report/<int:year>/<int:month>/', views.staff_monthly_report, name='staff_monthly_report_date'),

   path('staff/', views.staff, name='staff'),
   path('add-staff/', views.add_staff, name='add_staff'),
   path('edit-staff/<int:pk>/', views.edit_staff, name='edit_staff'),
   path('delete-staff/<int:pk>/', views.delete_staff, name='delete_staff'),
   path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
   path('edit-attendance/', views.edit_attendance, name='edit_attendance'),
   path('get-monthly-expenses/', views.get_monthly_expenses, name='get_monthly_expenses'),
]
