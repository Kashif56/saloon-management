# Generated by Django 5.1.4 on 2024-12-21 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_reason_expense_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
