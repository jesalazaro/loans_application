# payment_logic.py
from django.db import transaction
from django.db.models import Sum
from ..models import Customer, Loan, Payment, PaymentDetail
from django.utils import timezone
from rest_framework import serializers

def create_payment(validated_data):
    customer_external_id = validated_data.pop("customer_external_id", None)
    customer = Customer.objects.get(external_id=customer_external_id)

    validated_data["customer_id"] = customer
    validated_data["status"] = 1

    total_amount = validated_data["total_amount"]

    loans = Loan.objects.filter(
        customer_id=customer.id, outstanding__gt=0
    ).order_by("created_at")

    total_outstanding = loans.aggregate(total=Sum("outstanding"))["total"]
    if total_outstanding is None:
        total_outstanding = 0

    if total_amount > total_outstanding:
        raise serializers.ValidationError(
            "Total payment amount exceeds outstanding loan values"
        )

    with transaction.atomic():
        payment = Payment.objects.create(**validated_data)

        payment_details = []

        for loan in loans:
            payment_amount = min(total_amount, loan.outstanding)
            loan.outstanding -= payment_amount

            if loan.outstanding <= 0:
                loan.status = 4
            loan.save()

            payment_detail = PaymentDetail(
                amount=payment_amount, loand_id=loan, payment_id=payment
            )
            payment_details.append(payment_detail)
            total_amount -= payment_amount

        PaymentDetail.objects.bulk_create(payment_details)

    return payment
