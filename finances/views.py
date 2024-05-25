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
from rest_framework_api_key.permissions import HasAPIKey


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [HasAPIKey]

    # Use the custom serializer response, just to show the necessary fields
    def create(self, request):
        # Initialize the serializer with request data
        serializer = self.get_serializer(data=request.data)
        # Validate serializer data, raising an exception if validation fails
        serializer.is_valid(raise_exception=True)
        # Perform creation of the customer object
        self.perform_create(serializer)
        # Get headers for success response
        headers = self.get_success_headers(serializer.data)
        # Create a response serializer with the created instance
        response_serializer = CustomerCreateResponseSerializer(serializer.instance)
        # Return response with custom serializer data, status 201 (created), and headers
        return Response(response_serializer.data, status=201, headers=headers)


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [HasAPIKey]


class CustomerBalanceView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "external_id"
    permission_classes = [HasAPIKey]

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the customer object based on the provided external_id
        instance = self.get_object()
        # Initialize serializer with retrieved instance and request context
        serializer = self.get_serializer(instance, context={"request": request})
        # Return response with serialized customer data
        return Response(serializer.data)


class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCreateSerializer
    permission_classes = [HasAPIKey]


class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    permission_classes = [HasAPIKey]


class LoansByCustomerExternalIdView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        # Retrieve customer external_id from URL kwargs
        customer_external_id = self.kwargs["external_id"]
        # Get customer object based on external_id or return 404 if not found
        customer = get_object_or_404(Customer, external_id=customer_external_id)
        # Return queryset of loans filtered by customer_id
        return Loan.objects.filter(customer_id=customer.id)


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [HasAPIKey]
