from django.utils import timezone
from decimal import Decimal
from rest_framework import serializers
from .models import Customer, Loan, Payment, PaymentDetail
from django.db.models import Sum
from django.db import transaction

# serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["status", "total_debt", "available_amount"]

    # override the create method to set the status to 1:
    def create(self, validated_data):
        validated_data["status"] = 1
        return super().create(validated_data)

    def get_total_debt(self, obj):
        total_debt = Loan.objects.filter(customer_id=obj.id, status=1).aggregate(
            total_debt=Sum("outstanding")
        )["total_debt"]
        return total_debt if total_debt is not None else Decimal(0)

    def get_available_amount(self, obj):
        total_debt = self.get_total_debt(obj)
        avaliable_amount = obj.score - total_debt
        return avaliable_amount

    def to_representation(self, instance):
        data = {
            "external_id": instance.external_id,
            "score": instance.score,
            "total_debt": self.get_total_debt(instance),
            "available_amount": self.get_available_amount(instance),
        }
        return data


# Response custom fields
class CustomerCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["external_id", "status", "score", "preapproved_at"]


class LoanCreateSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Loan
        fields = ["external_id", "customer_external_id", "amount"]

    def create(self, validated_data):
        customer_external_id = validated_data.pop("customer_external_id")
        try:
            customer = Customer.objects.get(external_id=customer_external_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found")

        # check outstanding values
        outstanding_loans = Loan.objects.filter(
            customer_id=customer.id, status=2
        ).aggregate(Sum("outstanding"))

        if (outstanding_loans["outstanding__sum"] or 0) + validated_data[
            "amount"
        ] > customer.score:
            raise serializers.ValidationError(
                "Total outstanding loans exceed customer's credit score"
            )

        loan = Loan.objects.create(
            customer_id=customer,
            status=2,
            taken_at=timezone.now(),
            **validated_data,
            outstanding=validated_data.get("amount")
        )

        return loan


class LoanSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "external_id",
            "amount",
            "outstanding",
            "status",
            "customer_external_id",
        ]

    def get_customer_external_id(self, obj):
        return obj.customer_id.external_id


class PaymentSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Payment
        fields = ['customer_external_id', 'external_id', 'total_amount', 'status', 'paid_at']  

    def create(self, validated_data):
        customer_external_id = validated_data.pop("customer_external_id", None)
        customer = Customer.objects.get(external_id=customer_external_id)
        validated_data["customer_id"] = customer

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
            payment = super().create(validated_data)

            payment_details = []

            for loan in loans:
                if total_amount <= 0:
                    loan.status = 1
                    loan.save()
                    break

                payment_amount = min(total_amount, loan.outstanding)
                loan.outstanding -= payment_amount
                loan.save()

                payment_detail = PaymentDetail(
                    amount=payment_amount, loand_id=loan, payment_id=payment
                )
                payment_details.append(payment_detail)
                total_amount -= payment_amount

            PaymentDetail.objects.bulk_create(payment_details)

        return payment


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ['id', 'created_at', 'updated_at', 'amount', 'loand_id', 'payment_id']


