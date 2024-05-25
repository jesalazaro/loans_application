# loan_logic.py
from django.utils import timezone
from django.db.models import Sum
from rest_framework import serializers
from ..models import Customer, Loan


def create_loan(validated_data):
    # Obtain Customer_external_id
    customer_external_id = validated_data.pop("customer_external_id")
    # Get customer instance based on customer_external_id
    try:
        customer = Customer.objects.get(external_id=customer_external_id)
    except Customer.DoesNotExist:
        raise serializers.ValidationError("Customer not found")

    outstanding_loans = Loan.objects.filter(
        customer_id=customer.id, status=2
    ).aggregate(Sum("outstanding"))

    # Validate total outstanding loans against customer's credit score
    if (outstanding_loans["outstanding__sum"] or 0) + validated_data[
        "amount"
    ] > customer.score:
        raise serializers.ValidationError(
            "Total outstanding loans exceed customer's credit score"
        )

    # Create loan instance
    loan = Loan.objects.create(
        customer_id=customer,
        status=2,
        taken_at=timezone.now(),
        **validated_data,
        outstanding=validated_data.get("amount")
    )

    return loan
