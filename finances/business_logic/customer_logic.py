from decimal import Decimal
from django.db.models import Sum
from ..models import Loan


def get_total_debt(customer_id):
    # Calculate the total debt for the customer
    total_debt = Loan.objects.filter(customer_id=customer_id, status=1).aggregate(
        total_debt=Sum("outstanding")
    )["total_debt"]
    return total_debt if total_debt is not None else Decimal(0)


def get_available_amount(customer):
    # Calculate the available amount for the customer (score - total debt)
    total_debt = get_total_debt(customer.id)
    available_amount = customer.score - total_debt
    return available_amount
