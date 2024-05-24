from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics
from .models import Customer, Loan, Payment, PaymentDetail
from django.db.models import Sum
from .serializers import (
    CustomerCreateResponseSerializer,
    CustomerSerializer,
    LoanCreateSerializer,
    LoanSerializer,
    PaymentSerializer,
)
from django.db import transaction


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # Use the custom serializer response, just to show the necesary fields
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_serializer = CustomerCreateResponseSerializer(serializer.instance)
        return Response(response_serializer.data, status=201, headers=headers)


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerBalanceView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "external_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)


class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer


class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all


class LoansByCustomerExternalIdView(generics.ListAPIView):
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_external_id = self.kwargs["external_id"]
        customer = get_object_or_404(Customer, external_id=customer_external_id)
        return Loan.objects.filter(customer_id=customer.id)


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer