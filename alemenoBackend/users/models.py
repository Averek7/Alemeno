from django.db import models

class Customer(models.Model):
    Customer_ID = models.IntegerField(primary_key=True)
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    Age = models.IntegerField()
    PhoneNumber = models.CharField(max_length=20) 
    MonthlySalary = models.IntegerField()
    ApprovedLimit = models.IntegerField()

class Loan(models.Model):
    Loan_ID = models.AutoField(primary_key=True)
    Customer_ID = models.IntegerField()
    LoanAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Tenure = models.IntegerField()
    InterestRate = models.DecimalField(max_digits=5, decimal_places=2)
    MonthlyPayment = models.DecimalField(max_digits=10, decimal_places=2)
    EMIsOnTime = models.IntegerField()
    DateOfApproval = models.TextField()
    EndDate = models.TextField(null=True, blank=True)
