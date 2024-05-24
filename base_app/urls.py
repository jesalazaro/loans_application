"""
URL configuration for base_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from finances.views import  CustomerCreateView, CustomerBalanceView, CustomerListView, LoanCreateView, LoansByCustomerExternalIdView, PaymentListCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_customer/", CustomerCreateView.as_view(), name="create_customer"),
    path("get_customers/", CustomerListView.as_view(), name="customer_list"),
    path('get_customer_balance/<str:external_id>/', CustomerBalanceView.as_view(), name='customer-detail'),
    path('create_loan/', LoanCreateView.as_view(), name='loan-create'),
    path('getLoans/<str:external_id>/', LoansByCustomerExternalIdView.as_view(), name='get_loans_by_customer_external_id'),
    path('make_payment/', PaymentListCreateView.as_view(), name='make_payment'),
]
