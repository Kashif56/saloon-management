from django.db import models
from django.utils import timezone
from calendar import monthrange

STAFF_STATUS = (
    ('holiday', 'Holiday'),
    ('leave', 'Leave'),
    ('absent', 'Absent'),
    ('present', 'Present'),
)

APPOINMENT_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed')
)

EXPENSE_CATEGORIES = [
    ('salon_material', 'Salon Material'),
    ('supplies', 'Supplies'),
    ('other_purchases', 'Other Purchases'),
    ('marketing', 'Marketing'),
    ('commissions', 'Commissions'),
    ('salaries', 'Salaries'),
    ('rent', 'Rent'),
    ('electricity', 'Electricity'),
    ('other_utilities', 'Other Utilities'),
    ('tele_internet', 'Telephone & Internet'),
    ('legal', 'Legal & Professional'),
    ('cleaning', 'Cleaning'),
    ('others', 'Others'),
]

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Attendence(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STAFF_STATUS)
    period = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.staff.name} - {self.status}'

class Expense(models.Model):
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES, default='others')
    amount = models.PositiveIntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.description}"

class IncomeStatement(models.Model):
    period = models.DateField(unique=True, default=timezone.now)  # This enforces one statement per month
    total_sales = models.IntegerField(default=0)
    
    # Cost of Sales
    saloon_material = models.IntegerField(default=0)
    supplies = models.IntegerField(default=0)
    other_purchases = models.IntegerField(default=0)
    gross_profit = models.IntegerField(default=0)
    
    # Operating Expenses
    marketing = models.IntegerField(default=0)
    comissions = models.IntegerField(default=0)
    salaries = models.IntegerField(default=0)
    rent = models.IntegerField(default=0)
    electricity = models.IntegerField(default=0)
    other_utilities = models.IntegerField(default=0)
    tele_internet = models.IntegerField(default=0)
    legal = models.IntegerField(default=0)
    cleaning = models.IntegerField(default=0)
    others = models.IntegerField(default=0)
    net_income = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-period']
        
    def __str__(self):
        return f"Income Statement - {self.period.strftime('%B %Y')}"

    @property
    def get_total_expenses(self):
        return (
            self.saloon_material + self.supplies + self.other_purchases +
            self.marketing + self.comissions + self.salaries + self.rent +
            self.electricity + self.other_utilities + self.tele_internet +
            self.legal + self.cleaning + self.others
        )

    def save(self, *args, **kwargs):
        # Calculate gross profit
        self.gross_profit = self.total_sales - (self.saloon_material + self.supplies + self.other_purchases)
        
        # Calculate net income before saving
        self.net_income = self.total_sales - self.get_total_expenses
        super().save(*args, **kwargs)

class Appointments(models.Model):
    name = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    service = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=APPOINMENT_STATUS)
    time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workflow(models.Model):
    artist = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    service = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=1)
    period = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.artist.name