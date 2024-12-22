from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Staff, Expense, IncomeStatement, Appointments, Attendence, Workflow, EXPENSE_CATEGORIES

from datetime import date, datetime, timedelta
from calendar import monthrange
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse

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
    expenses_qs = Expense.objects.all().order_by('-date')
    categories = dict(EXPENSE_CATEGORIES)

    context = {
        "expenses": expenses_qs,
        "categories": EXPENSE_CATEGORIES,
    }
    return render(request, 'expenses.html', context)

def add_expense(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        expense = Expense(
            description=description,
            category=category,
            amount=amount,
            date=date
        )
        expense.save()
        messages.success(request, 'Expense added successfully!')
        return redirect('core:expenses')
    
    return redirect('core:expenses')

def edit_expense(request, pk):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk)
        expense.description = request.POST.get('description')
        expense.category = request.POST.get('category')
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
    if request.method == 'POST':
        # Get form data
        total_sales = request.POST.get('total_sales', 0)
        period = request.POST.get('period')
        
        try:
            # Convert period string (YYYY-MM) to date object (YYYY-MM-01)
            period_date = datetime.strptime(f"{period}-01", '%Y-%m-%d').date()
            
            # Check if statement already exists for this month
            existing_statement = IncomeStatement.objects.filter(period=period_date).first()
            if existing_statement:
                messages.error(request, f'An income statement for {period_date.strftime("%B %Y")} already exists!')
                return redirect('core:income_statement')
            
            # Get month start and end dates
            month_start = period_date.replace(day=1)
            month_end = month_start.replace(day=monthrange(period_date.year, period_date.month)[1])
            
            # Get expenses for this month grouped by category
            monthly_expenses = (
                Expense.objects
                .filter(date__range=[month_start, month_end])
                .values('category')
                .annotate(total=Sum('amount'))
            )
            
            # Create a dictionary to store expense totals by category
            expense_totals = {category[0]: 0 for category in EXPENSE_CATEGORIES}
            for expense in monthly_expenses:
                expense_totals[expense['category']] = expense['total']
            
            # Create new income statement
            statement = IncomeStatement(period=period_date)
            
            # Update fields
            statement.total_sales = int(total_sales)
            statement.saloon_material = int(request.POST.get('saloon_material', expense_totals.get('salon_material', 0)))
            statement.supplies = int(request.POST.get('supplies', expense_totals.get('supplies', 0)))
            statement.other_purchases = int(request.POST.get('other_purchases', expense_totals.get('other_purchases', 0)))
            statement.marketing = int(request.POST.get('marketing', expense_totals.get('marketing', 0)))
            statement.comissions = int(request.POST.get('comissions', expense_totals.get('commissions', 0)))
            statement.salaries = int(request.POST.get('salaries', expense_totals.get('salaries', 0)))
            statement.rent = int(request.POST.get('rent', expense_totals.get('rent', 0)))
            statement.electricity = int(request.POST.get('electricity', expense_totals.get('electricity', 0)))
            statement.other_utilities = int(request.POST.get('other_utilities', expense_totals.get('other_utilities', 0)))
            statement.tele_internet = int(request.POST.get('tele_internet', expense_totals.get('tele_internet', 0)))
            statement.legal = int(request.POST.get('legal', expense_totals.get('legal', 0)))
            statement.cleaning = int(request.POST.get('cleaning', expense_totals.get('cleaning', 0)))
            statement.others = int(request.POST.get('others', expense_totals.get('others', 0)))
            
            statement.save()
            
            messages.success(request, f'Income statement for {period_date.strftime("%B %Y")} saved successfully!')
            return redirect('core:income_statement')
            
        except ValueError:
            messages.error(request, 'Invalid data provided. Please check your inputs.')
            return redirect('core:income_statement')
    
    # Get statements for display
    statements = IncomeStatement.objects.all()
    
    context = {
        'statements': statements,
        'current_month': timezone.now().date()
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
        
        # Cost of Sales
        statement.saloon_material = int(request.POST.get('saloon_material'))
        statement.supplies = int(request.POST.get('supplies'))
        statement.other_purchases = int(request.POST.get('other_purchases'))
        statement.gross_profit = int(request.POST.get('gross_profit'))
        
        # Operating Expenses
        statement.marketing = int(request.POST.get('marketing'))
        statement.comissions = int(request.POST.get('comissions'))
        statement.salaries = int(request.POST.get('salaries'))
        statement.rent = int(request.POST.get('rent'))
        statement.electricity = int(request.POST.get('electricity'))
        statement.other_utilities = int(request.POST.get('other_utilities'))
        statement.tele_internet = int(request.POST.get('tele_internet'))
        statement.legal = int(request.POST.get('legal'))
        statement.cleaning = int(request.POST.get('cleaning'))
        statement.others = int(request.POST.get('others'))
        statement.net_income = int(request.POST.get('net_income'))
        
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


def workflow(request):
    # Get selected date from query parameters or use current date
    current_date = timezone.now()
    selected_date = request.GET.get('date')
    
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            # Don't allow future dates
            if selected_date > current_date.date():
                selected_date = current_date.date()
        except ValueError:
            selected_date = current_date.date()
    else:
        selected_date = current_date.date()
    
    # Calculate previous and next dates
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    # Disable next date if it's beyond current date
    show_next = next_date <= current_date.date()
    
    # Get all active staff members
    staff_members = Staff.objects.filter(is_active=True)
    
    # Initialize data structure for staff information
    staff_data = []
    total_today_sales = 0
    
    # Get attendance records for today
    attendance_records = Attendence.objects.filter(period=selected_date)
    attendance_dict = {att.staff_id: att.status for att in attendance_records}
    
    for staff in staff_members:
        # Get workflow entries for selected date
        today_workflows = Workflow.objects.filter(
            artist=staff,
            period=selected_date
        ).order_by('-created_at')
        
        # Calculate total sales for this staff member
        today_sales = sum(workflow.amount for workflow in today_workflows)
        total_today_sales += today_sales
        
        # Get appointments count
        today_appointments = Appointments.objects.filter(
            time__date=selected_date
        ).count()
        
        # Get attendance status
        is_present = attendance_dict.get(staff.id, False)
        
        staff_data.append({
            'staff': staff,
            'today_sales': today_sales,
            'appointments_count': today_appointments,
            'workflows': today_workflows,
            'is_present': is_present
        })
    
    # Calculate percentages
    for data in staff_data:
        if total_today_sales > 0:
            data['percentage'] = round((data['today_sales'] / total_today_sales) * 100, 1)
        else:
            data['percentage'] = 0
    
    context = {
        'staff_data': staff_data,
        'total_today_sales': total_today_sales,
        'current_date': current_date,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'show_next': show_next,
        'staff_list': staff_members,
    }
    
    return render(request, 'workflow.html', context)

def add_workflow(request):
    if request.method == 'POST':
        artist_id = request.POST.get('artist')
        service = request.POST.get('service')
        amount = request.POST.get('amount')
        period = request.POST.get('period')
        
        try:
            artist = Staff.objects.get(id=artist_id)
            period_date = datetime.strptime(period, '%Y-%m-%d').date()
            
            # Don't allow future dates
            if period_date > timezone.now().date():
                messages.error(request, 'Cannot add workflow for future dates.')
                return redirect(f'/workflow/?date={period}')
            
            Workflow.objects.create(
                artist=artist,
                service=service,
                amount=float(amount),
                period=period_date
            )
            
            messages.success(request, 'Workflow added successfully!')
        except (Staff.DoesNotExist, ValueError) as e:
            messages.error(request, 'Error adding workflow. Please try again.')
        
        # Redirect back to the workflow page for the same date
        return redirect(f'/workflow/?date={period}')


def staff_monthly_report(request, staff_id, year=None, month=None):
    staff = get_object_or_404(Staff, id=staff_id)
    today = timezone.now()
    
    if year is None or month is None:
        year = today.year
        month = today.month
    
    # Don't allow future dates
    future_date = False
    if year > today.year or (year == today.year and month > today.month):
        year = today.year
        month = today.month
        future_date = True
        messages.warning(request, "Cannot view future months. Showing current month instead.")
    
    # Get all workflows for the specified month
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    workflows = Workflow.objects.filter(
        artist=staff,
        period__gte=start_date,
        period__lt=end_date
    ).order_by('period', '-created_at')
    
    # Calculate totals and averages
    total_sales = sum(workflow.amount for workflow in workflows)
    workflows_count = workflows.count()
    avg_per_service = total_sales // workflows_count if workflows_count > 0 else 0
    
    # Group workflows by date
    daily_workflows = {}
    for workflow in workflows:
        day = workflow.period
        if day not in daily_workflows:
            daily_workflows[day] = {
                'workflows': [],
                'total': 0
            }
        daily_workflows[day]['workflows'].append(workflow)
        daily_workflows[day]['total'] += workflow.amount
    
    context = {
        'staff_list': Staff.objects.filter(is_active=True),
        'staff': staff,
        'year': year,
        'month': month,
        'month_name': start_date.strftime('%B'),
        'total_sales': total_sales,
        'workflows_count': workflows_count,
        'daily_workflows': sorted(daily_workflows.items()),
        'average_per_service': avg_per_service,
        'show_next': not (year == today.year and month == today.month)  # Only show next if not current month
    }
    
    return render(request, 'staff_monthly_report.html', context)

def monthly_report(request, year=None, month=None):
    # Get year and month from query parameters or use current date
    today = timezone.now()
    
    if year is None or month is None:
        year = today.year
        month = today.month
    
    # Don't allow future dates
    future_date = False
    if year > today.year or (year == today.year and month > today.month):
        year = today.year
        month = today.month
        future_date = True
        messages.warning(request, "Cannot view future months. Showing current month instead.")
    
    # Get all active staff members
    staff_members = Staff.objects.filter(is_active=True)
    
    # Get all workflows for the specified month
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Initialize data structure for staff information
    staff_data = []
    total_month_sales = 0
    
    for staff in staff_members:
        workflows = Workflow.objects.filter(
            artist=staff,
            period__gte=start_date,
            period__lt=end_date
        ).order_by('period', '-created_at')
        
        # Calculate total sales for this staff member
        staff_total = sum(workflow.amount for workflow in workflows)
        total_month_sales += staff_total
        workflows_count = workflows.count()
        
        # Calculate average per service
        avg_per_service = staff_total // workflows_count if workflows_count > 0 else 0
        
        # Group workflows by date
        daily_workflows = {}
        for workflow in workflows:
            day = workflow.period
            if day not in daily_workflows:
                daily_workflows[day] = {
                    'workflows': [],
                    'total': 0
                }
            daily_workflows[day]['workflows'].append(workflow)
            daily_workflows[day]['total'] += workflow.amount
        
        staff_data.append({
            'staff': staff,
            'total_sales': staff_total,
            'workflows_count': workflows_count,
            'daily_workflows': sorted(daily_workflows.items()),
            'average_per_service': avg_per_service,
            'percentage': 0  # Will be calculated after all staff are processed
        })
    
    # Sort staff by total sales (highest first)
    staff_data.sort(key=lambda x: x['total_sales'], reverse=True)
    
    # Calculate percentages
    for data in staff_data:
        if total_month_sales > 0:
            data['percentage'] = round((data['total_sales'] / total_month_sales) * 100, 1)
    
    context = {
        'staff_data': staff_data,
        'staff_list': staff_members,
        'year': year,
        'month': month,
        'month_name': start_date.strftime('%B'),
        'total_month_sales': total_month_sales,
        'total_services': sum(data['workflows_count'] for data in staff_data),
        'show_next': not (year == today.year and month == today.month)  # Only show next if not current month
    }
    
    return render(request, 'monthly_report.html', context)

def get_workflow(request, workflow_id):
    """Get workflow data for editing"""
    workflow = get_object_or_404(Workflow, id=workflow_id)
    data = {
        'id': workflow.id,
        'artist_id': workflow.artist.id,
        'service': workflow.service,
        'amount': workflow.amount,
        'period': workflow.period.strftime('%Y-%m-%d')
    }
    return JsonResponse(data)

def edit_workflow(request, workflow_id):
    """Edit workflow via AJAX"""
    workflow = get_object_or_404(Workflow, id=workflow_id)
    
    if request.method == 'POST':
        try:
            artist = Staff.objects.get(id=request.POST.get('artist'))
            period_date = datetime.strptime(request.POST.get('period'), '%Y-%m-%d').date()
            
            # Don't allow future dates
            if period_date > timezone.now().date():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot add workflow for future dates.'
                })
            
            workflow.artist = artist
            workflow.service = request.POST.get('service')
            workflow.amount = float(request.POST.get('amount'))
            workflow.period = period_date
            workflow.save()

            messages.success(request, 'Workflow updated successfully!')
            
            return JsonResponse({
                'status': 'success',
                'message': 'Workflow updated successfully!',
                'data': {
                    'id': workflow.id,
                    'artist_name': workflow.artist.name,
                    'service': workflow.service,
                    'amount': workflow.amount,
                    'period': workflow.period.strftime('%Y-%m-%d')
                }
            })
        except (Staff.DoesNotExist, ValueError) as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Error updating workflow. Please try again.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_workflow(request, workflow_id):
    """Delete workflow via AJAX"""
    workflow = get_object_or_404(Workflow, id=workflow_id)
    
    try:
        workflow.delete()
        messages.success(request, 'Workflow deleted successfully!')
        return JsonResponse({
            'status': 'success',
            'message': 'Workflow deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Error deleting workflow. Please try again.'
        })

def get_monthly_expenses(request):
    period = request.GET.get('period')
    
    try:
        # Convert period string (YYYY-MM) to date object (YYYY-MM-01)
        period_date = datetime.strptime(f"{period}-01", '%Y-%m-%d').date()
        
        # Get month start and end dates
        month_start = period_date.replace(day=1)
        month_end = month_start.replace(day=monthrange(period_date.year, period_date.month)[1])
        
        # Get expenses for this month grouped by category
        monthly_expenses = (
            Expense.objects
            .filter(date__range=[month_start, month_end])
            .values('category')
            .annotate(total=Sum('amount'))
        )
        
        # Create a dictionary to store expense totals by category
        expense_totals = {category[0]: 0 for category in EXPENSE_CATEGORIES}
        for expense in monthly_expenses:
            expense_totals[expense['category']] = expense['total']
            
        return JsonResponse({'success': True, 'expenses': expense_totals})
        
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid date format'})
