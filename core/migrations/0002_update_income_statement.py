from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomestatement',
            name='cost_of_product',
        ),
        migrations.RemoveField(
            model_name='incomestatement',
            name='operating_expenses',
        ),
        migrations.RemoveField(
            model_name='incomestatement',
            name='tax',
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='cleaning',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='electricity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='legal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='marketing',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='other_purchases',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='other_utilities',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='saloon_material',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='supplies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incomestatement',
            name='tele_internet',
            field=models.IntegerField(default=0),
        ),
    ]
