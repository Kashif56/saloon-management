from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Staff, Expense, IncomeStatement, Appointments, Attendence

from datetime import date, datetime, timedelta
from calendar import monthrange
from django.db.models import Count
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'index.html')

# def attendance_page(request):

#     # Get the current year and month
#     today = date.today()
#     year = today.year
#     month = today.month

#     # Get the days of the current month
#     days_in_month = monthrange(year, month)[1]
#     days_of_month = [str(day).zfill(2) for day in range(1, days_in_month + 1)]  # List of days (e.g., ['01', '02', '03'])

    
#     staff_list = Staff.objects.all()

#     context = {
#         "days_of_month": days_of_month,
#         "staff_list": staff_list,
#     }


#     return render(request, 'attendence_page.html', context)



def expenses_page(request):
    expenses_qs = Expense.objects.all()

    context = {
        "expenses": expenses_qs,
    }
    return render(request, 'expenses.html', context)

def add_expense(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

       
        expense = Expense(
            description=description,
            amount=amount,
            date=date
        )
        expense.save()
        return redirect('core:expenses')
         
    
    return redirect('core:expenses')

def edit_expense(request, pk):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk)
        expense.description = request.POST.get('description')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('core:expenses')
    return redirect('core:expenses')

def delete_expense(request, pk):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
    return redirect('core:expenses')

def income_statement(request):
    statements = IncomeStatement.objects.all()
    context = {
        "income_statements": statements
    }
    return render(request, 'income_statement.html', context)

def income_statement_detail(request, pk):
    statement = get_object_or_404(IncomeStatement, pk=pk)
    context = {
        "statement": statement
    }
    return render(request, 'income_statement_detail.html', context)

def add_statement(request):
    if request.method == 'POST':
        # Get all the form data
        period = request.POST.get('period')
        # Convert YYYY-MM format to YYYY-MM-01 for database storage
        period = f"{period}-01" if period else None
        
        total_sales = int(request.POST.get('total_sales'))
        cost_of_product = int(request.POST.get('cost_of_product'))
        operating_expenses = int(request.POST.get('operating_expenses'))
        salaries = int(request.POST.get('salaries'))
        comissions = int(request.POST.get('comissions'))
        rent = int(request.POST.get('rent'))
        tax = int(request.POST.get('tax'))
        others = int(request.POST.get('others'))

        # Create and save the statement
        statement = IncomeStatement(
            period=period,
            total_sales=total_sales,
            cost_of_product=cost_of_product,
            operating_expenses=operating_expenses,
            salaries=salaries,
            comissions=comissions,
            rent=rent,
            tax=tax,
            others=others
        )
        statement.save()  # This will automatically calculate gross_profit and net_income
        
        return redirect('core:income_statement')
    
    return redirect('core:income_statement')

def edit_statement(request, pk):
    if request.method == 'POST':
        statement = get_object_or_404(IncomeStatement, pk=pk)
        statement.period = f"{request.POST.get('period')}-01"
        statement.total_sales = int(request.POST.get('total_sales'))
        statement.cost_of_product = int(request.POST.get('cost_of_product'))
        statement.operating_expenses = int(request.POST.get('operating_expenses'))
        statement.salaries = int(request.POST.get('salaries'))
        statement.comissions = int(request.POST.get('comissions'))
        statement.rent = int(request.POST.get('rent'))
        statement.tax = int(request.POST.get('tax'))
        statement.others = int(request.POST.get('others'))
        statement.save()
        messages.success(request, 'Income statement updated successfully!')
        return redirect('core:income_statement')
    return redirect('core:income_statement')

def delete_statement(request, pk):
    if request.method == 'POST':
        statement = get_object_or_404(IncomeStatement, pk=pk)
        statement.delete()
        messages.success(request, 'Income statement deleted successfully!')
    return redirect('core:income_statement')

def appointments(request):
    appointments_qs = Appointments.objects.all()
    context = {
        "appointments": appointments_qs
    }
    return render(request, 'appoinments.html', context)

def add_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reference = request.POST.get('reference')
        contact = request.POST.get('contact')
        time = request.POST.get('time')
        service = request.POST.get('service', '')  # Optional field
        
        appointment = Appointments(
            name=name,
            reference=reference,
            contact=contact,
            time=time,
            service=service,
            status='pending'  # Default status
        )
        appointment.save()
        return redirect('core:appointments')
    
    return redirect('core:appointments')

def edit_appointment(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointments, pk=pk)
        appointment.name = request.POST.get('name')
        appointment.reference = request.POST.get('reference')
        appointment.contact = request.POST.get('contact')
        appointment.service = request.POST.get('service')
        appointment.time = request.POST.get('time')
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('core:appointments')
    return redirect('core:appointments')

def delete_appointment(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointments, pk=pk)
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
    return redirect('core:appointments')

def workflow(request):
    pass


def staff(request):
    staff_list = Staff.objects.all()
    context = {
        "staff_list": staff_list
    }
    return render(request, 'staff.html', context)

def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
    
        staff = Staff(
            name=name,
            role=role
        )
        staff.save()
    
    return redirect('core:staff')

def edit_staff(request, pk):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, pk=pk)
        staff.name = request.POST.get('name')
        staff.role = request.POST.get('role')
        staff.save()
        messages.success(request, 'Staff member updated successfully!')
        return redirect('core:staff')
    return redirect('core:staff')

def delete_staff(request, pk):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, pk=pk)
        staff.delete()
        messages.success(request, 'Staff member deleted successfully!')
    return redirect('core:staff')

def attendance(request):
    # Get selected month or default to current month
    today = timezone.now()
    selected_month = request.GET.get('month')
    
    if selected_month:
        year, month = map(int, selected_month.split('-'))
        current_month = today.replace(year=year, month=month, day=1)
    else:
        current_month = today.replace(day=1)
    
    # Get month range
    _, last_day = monthrange(current_month.year, current_month.month)
    month_end = current_month.replace(day=last_day)

    # Get all days in selected month
    days = []
    current_date = current_month
    while current_date <= month_end:
        days.append(current_date)
        current_date += timedelta(days=1)

    # Get available months for selector (last 12 months)
    available_months = []
    for i in range(12):
        month_date = today.replace(day=1) - timedelta(days=i*30)
        if month_date not in available_months:
            available_months.append(month_date)
    available_months.sort(reverse=True)

    # Get all staff and their attendance
    staff_list = Staff.objects.filter(is_active=True)
    staff_attendance = []

    for staff in staff_list:
        # Get attendance records for selected month
        attendance_records = Attendence.objects.filter(
            staff=staff,
            period__gte=current_month,
            period__lte=month_end
        )

        # Create attendance status dictionary
        attendance_status = {record.period: record.status for record in attendance_records}
        
        # Build attendance list for all days
        attendance_list = []
        for day in days:
            status = attendance_status.get(day.date(), '')
            attendance_list.append({'date': day, 'status': status})

        staff_attendance.append({
            'name': staff.name,
            'role': staff.role,
            'attendance': attendance_list,
            'summary': {
                'present': attendance_records.filter(status='present').count(),
                'absent': attendance_records.filter(status='absent').count(),
                'leave': attendance_records.filter(status='leave').count(),
                'holiday': attendance_records.filter(status='holiday').count(),
                'total_days': len(days),
                'attendance_percentage': round(
                    (attendance_records.filter(status='present').count() / len(days)) * 100 
                    if len(days) > 0 else 0, 1
                )
            }
        })

    context = {
        'selected_month': current_month.strftime('%Y-%m'),
        'month': current_month,
        'available_months': available_months,
        'days': days,
        'staff_list': staff_list,
        'staff_attendance': staff_attendance
    }
    return render(request, 'attendence_page.html', context)

def mark_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        staff_list = Staff.objects.filter(is_active=True)

        for staff in staff_list:
            status = request.POST.get(f'status_{staff.id}')
            if status:
                # Update or create attendance record
                Attendence.objects.update_or_create(
                    staff=staff,
                    period=date,
                    defaults={'status': status}
                )

        messages.success(request, 'Attendance marked successfully!')
        return redirect('core:attendance')

    return redirect('core:attendance')

def edit_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        staff_name = request.POST.get('staff_name')
        status = request.POST.get('status')

        try:
            staff = Staff.objects.get(name=staff_name)
            # Update or create attendance record
            Attendence.objects.update_or_create(
                staff=staff,
                period=date,
                defaults={'status': status}
            )
            messages.success(request, f'Attendance updated for {staff_name} on {date}')
        except Staff.DoesNotExist:
            messages.error(request, f'Staff member {staff_name} not found')
        
        return redirect('core:attendance')

    return redirect('core:attendance')