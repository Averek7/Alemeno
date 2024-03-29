# Generated by Django 5.0.1 on 2024-02-05 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('Customer_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=255)),
                ('LastName', models.CharField(max_length=255)),
                ('Age', models.IntegerField()),
                ('PhoneNumber', models.CharField(max_length=20)),
                ('MonthlySalary', models.IntegerField()),
                ('ApprovedLimit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('Loan_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('LoanAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Tenure', models.IntegerField()),
                ('InterestRate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('MonthlyPayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('EMIsOnTime', models.IntegerField()),
                ('DateOfApproval', models.DateField()),
                ('EndDate', models.DateField(blank=True, null=True)),
                ('Customer_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
        ),
    ]
