from django.db import models



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
    amount = models.PositiveIntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.description

class IncomeStatement(models.Model):
    total_sales = models.IntegerField(default=0)
    cost_of_product = models.IntegerField(default=0)
    gross_profit = models.IntegerField(default=0)
    operating_expenses = models.IntegerField(default=0)
    comissions = models.IntegerField(default=0)
    salaries = models.IntegerField(default=0)
    rent = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    others = models.IntegerField(default=0)
    net_income = models.IntegerField(default=0)

    period = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f'Income Statement for {self.period}'

    def get_total_expenses(self):
        expenses = 0
        expenses += self.operating_expenses
        expenses += self.salaries
        expenses += self.comissions
        expenses += self.rent
        expenses += self.tax
        expenses += self.others
        expenses += self.cost_of_product

        return expenses


    def save(self, *args, **kwargs):
        self.gross_profit = self.total_sales - self.cost_of_product

        total_expenses = self.get_total_expenses()

        self.net_income = self.total_sales - total_expenses

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
