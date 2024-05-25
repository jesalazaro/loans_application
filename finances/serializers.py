from rest_framework import serializers
from finances.business_logic.customer_logic import get_available_amount, get_total_debt
from finances.business_logic.loan_logic import create_loan
from finances.business_logic.payment_logic import create_payment
from .models import Customer, Loan, Payment, PaymentDetail



# serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField(write_only=True)
    total_debt = serializers.SerializerMethodField(read_only=True)
    available_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["status"]
    
    def create(self, validated_data):
        validated_data["status"] = 1
        return super().create(validated_data)

    def get_total_debt(self, obj):
        return get_total_debt(obj.id)

    def get_available_amount(self, obj):
        return get_available_amount(obj)

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
    # Obtain Customer_external_id
    customer_external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Loan
        fields = ["external_id", "customer_external_id", "amount"]

    def create(self, validated_data):
        return create_loan(validated_data)


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
    # Obtain Customer_external_id
    customer_external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Payment
        fields = [
            "customer_external_id",
            "external_id",
            "total_amount",
            "paid_at",
        ]

    def create(self, validated_data):
        return create_payment(validated_data)


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ["id", "created_at", "updated_at", "amount", "loand_id", "payment_id"]
