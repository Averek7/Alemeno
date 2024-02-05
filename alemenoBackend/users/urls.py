from django.urls import path
from .views import (
    CustomerCreateView,
    LoanEligibilityCheckView,
    LoanCreateView,
    LoanRetrieveView,
    LoanListByCustomerView,
    LoanListView,
    CustomerListView
)

urlpatterns = [
    path('register/', CustomerCreateView.as_view(), name='customer-create'),
    path('check-eligibility/', LoanEligibilityCheckView.as_view(), name='loan-eligibility-check'),
    path('create-loan/', LoanCreateView.as_view(), name='create-loan'),
    path('view-loan/<int:pk>/', LoanRetrieveView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>/', LoanListByCustomerView.as_view(), name='view-loans'),
    path('loans/', LoanListView.as_view(), name='loans'),
    path('customers/', CustomerListView.as_view(), name='customers')
]
