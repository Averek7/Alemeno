from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from datetime import date
from django.http import Http404
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        monthly_salary = serializer.validated_data['MonthlySalary']
        approved_limit = round(36 * monthly_salary, -5);
        
        customer = serializer.save(ApprovedLimit=approved_limit)

        response_data = {
            'customer_id': customer.Customer_ID,
            'name': customer.FirstName + ' ' + customer.LastName,
            'age': customer.Age,
            'monthly_salary': customer.MonthlySalary,
            'approved_limit': customer.ApprovedLimit,
            'phone_number': customer.PhoneNumber,
        }  

        return Response(response_data, status=status.HTTP_201_CREATED)

class LoanEligibilityCheckView(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data['Customer_ID']
        loan_amount = serializer.validated_data['LoanAmount']
        interest_rate = serializer.validated_data['InterestRate']

        try:
           # Fetch customer and their existing loans
           customer = Customer.objects.get(Customer_ID=customer_id)
           print(customer)
           current_loans = Loan.objects.get(Customer_ID=customer_id)
           print(current_loans)
           credit_score = self.calculate_credit_score(customer, current_loans)
           approval, corrected_interest_rate = self.check_loan_eligibility(credit_score, interest_rate, customer)
           response_data = {
               'customer_id': customer_id,
               'approval': approval,
               'interest_rate': interest_rate,
               'corrected_interest_rate': corrected_interest_rate,
               'tenure': serializer.validated_data['Tenure'],
               'monthly_installment': self.calculate_monthly_installment(loan_amount, interest_rate, serializer.validated_data['Tenure']),
           }
   
           return Response(response_data, status=status.HTTP_200_OK)
        
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        except Customer.DoesNotExist:
            # If customer does not exist, return a specific response
            return Response({'error': 'Customer does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Customer.MultipleObjectsReturned:
            # If multiple customers match the criteria, return a specific response
            return Response({'error': 'Multiple customers with the same ID found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_credit_score(self, customer, current_loans):
        paid_on_time_score = sum([loan.EMIsOnTime for loan in current_loans])
        num_loans_score = current_loans.count()
        loan_activity_score = sum([1 for loan in current_loans if loan.DateOfApproval.year == date.today().year])
        loan_approved_volume_score = sum([loan.LoanAmount for loan in current_loans])
        sum_current_loans = current_loans.aggregate(Sum('LoanAmount'))['LoanAmount__sum'] or 0

        # If sum of current loans > approved limit, credit score = 0
        if sum_current_loans > customer.ApprovedLimit:
            credit_score = 0
        else:
            credit_score = paid_on_time_score + num_loans_score + loan_activity_score + loan_approved_volume_score

        return credit_score

    def check_loan_eligibility(self, credit_score, interest_rate, customer):
        if credit_score > 50:
            return True, interest_rate  # Approve loan
        elif 50 > credit_score > 30:
            corrected_interest_rate = max(interest_rate, 12.0)  # Set interest rate to 12% if lower
            return True, corrected_interest_rate
        elif 30 > credit_score > 10:
            corrected_interest_rate = max(interest_rate, 16.0)  # Set interest rate to 16% if lower
            return True, corrected_interest_rate
        elif 10 > credit_score:
            return False, None  # Don't approve any loans
        else:
            return False, None

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        # Sample calculation (adjust based on your requirements)
        monthly_interest_rate = interest_rate / 100 / 12
        numerator = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure
        denominator = (1 + monthly_interest_rate) ** tenure - 1
        monthly_installment = round(numerator / denominator, 2)
        return monthly_installment


class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data['Customer_ID']
        loan_amount = serializer.validated_data['LoanAmount']
        interest_rate = serializer.validated_data['InterestRate']
        tenure = serializer.validated_data['Tenure']

        # Fetch customer and their existing loans
        customer = Customer.objects.get(Customer_ID=customer_id)
        current_loans = Loan.objects.filter(Customer_ID=customer_id)

        # Calculate credit score based on the provided components
        credit_score = self.calculate_credit_score(customer, current_loans)

        # Check loan eligibility based on credit score
        approval, corrected_interest_rate = self.check_loan_eligibility(credit_score, interest_rate, customer)

        # Prepare the response
        if approval:
            # If loan is approved, create a new loan
            new_loan = Loan.objects.create(
                Customer_ID=customer,
                LoanAmount=loan_amount,
                InterestRate=corrected_interest_rate,
                Tenure=tenure,
                MonthlyPayment=self.calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure),
            )

            response_data = {
                'loan_id': new_loan.Loan_ID,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': 'Loan approved',
                'monthly_installment': new_loan.MonthlyPayment,
            }
        else:
            response_data = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': 'Loan not approved',
                'monthly_installment': None,
            }

        return Response(response_data, status=status.HTTP_200_OK)

class LoanRetrieveView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def retrieve(self, request, *args, **kwargs):
       loan_id = kwargs.get('pk')
       
       try:
        loan = Loan.objects.get(Loan_ID=loan_id)
        customer_details = {
                'id': loan.Customer_ID.Customer_ID,
                'first_name': loan.Customer_ID.FirstName,
                'last_name': loan.Customer_ID.LastName,
                'phone_number': loan.Customer_ID.PhoneNumber,
                'age': loan.Customer_ID.Age,
            }
        response_data = {
                'loan_id': loan.Loan_ID,
                'customer': customer_details,
                'loan_amount': loan.LoanAmount,
                'interest_rate': loan.InterestRate,
                'monthly_installment': loan.MonthlyPayment,
                'tenure': loan.Tenure,
            }
        return Response(response_data, status=status.HTTP_200_OK)

       except Loan.DoesNotExist:
        raise Http404("Loan does not exist.")

       except Loan.MultipleObjectsReturned:
        loans = Loan.objects.filter(Loan_ID=loan_id)
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoanListByCustomerView(generics.ListAPIView):
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        # Add distinct() to ensure only distinct records are fetched
        return Loan.objects.filter(Customer_ID=customer_id).distinct('Loan_ID', 'Customer_ID')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer