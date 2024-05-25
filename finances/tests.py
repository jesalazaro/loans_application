from decimal import Decimal
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from finances.business_logic.customer_logic import get_available_amount, get_total_debt
from finances.business_logic.loan_logic import create_loan
from finances.business_logic.payment_logic import create_payment
from finances.models import Customer, Loan, Payment, PaymentDetail
from rest_framework import serializers

# Create your tests here.

from django.test import TestCase
from finances.models import (
    Customer,
)  # Update the import to reflect the actual path of the model
from django.utils import timezone

from finances.serializers import (
    CustomerSerializer,
    LoanCreateSerializer,
    PaymentSerializer,
)


class CustomerModelTest(TestCase):

    def setUp(self):
        # Setup runs before each test
        self.customer = Customer.objects.create(
            external_id="unique_id_123",
            status=1,
            score=85.50,
        )

    def test_customer_creation(self):
        # Test if the customer instance is created correctly
        customer = self.customer
        self.assertTrue(isinstance(customer, Customer))
        self.assertEqual(customer.external_id, "unique_id_123")
        self.assertEqual(customer.status, 1)
        self.assertEqual(customer.score, 85.50)

    def test_created_at_auto_now_add(self):
        # Test if created_at is set automatically
        customer = self.customer
        self.assertIsNotNone(customer.created_at)
        self.assertTrue(
            (timezone.now() - customer.created_at).total_seconds() < 10
        )  # Within 10 seconds

    def test_updated_at_auto_now(self):
        # Test if updated_at is set automatically and updates correctly
        customer = self.customer
        original_updated_at = customer.updated_at
        customer.status = 2
        customer.save()
        self.assertNotEqual(customer.updated_at, original_updated_at)

    def test_external_id_unique(self):
        # Test that the external_id field is unique
        with self.assertRaises(Exception):
            Customer.objects.create(
                external_id="unique_id_123",  # Duplicate external_id
                status=2,
                score=90.00,
            )

    def test_preapproved_at_null(self):
        # Test that preapproved_at can be null
        customer = self.customer
        self.assertIsNone(customer.preapproved_at)
        customer.preapproved_at = timezone.now()
        customer.save()
        self.assertIsNotNone(customer.preapproved_at)


class PaymentModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="customer_id_123",
            status=1,
            score=85.50,
        )
        self.payment = Payment.objects.create(
            external_id="payment_id_123",
            total_amount=100.1234567890,
            status=1,
            customer_id=self.customer,
        )

    def test_payment_creation(self):
        payment = self.payment
        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(payment.external_id, "payment_id_123")
        self.assertEqual(payment.total_amount, 100.1234567890)
        self.assertEqual(payment.status, 1)
        self.assertEqual(payment.customer_id, self.customer)

    def test_created_at_auto_now_add(self):
        payment = self.payment
        self.assertIsNotNone(payment.created_at)
        self.assertTrue((timezone.now() - payment.created_at).total_seconds() < 10)

    def test_updated_at_auto_now(self):
        payment = self.payment
        original_updated_at = payment.updated_at
        payment.status = 2
        payment.save()
        self.assertNotEqual(payment.updated_at, original_updated_at)

    def test_external_id_unique(self):
        with self.assertRaises(Exception):
            Payment.objects.create(
                external_id="payment_id_123",  # Duplicate external_id
                total_amount=200.1234567890,
                status=2,
                customer_id=self.customer,
            )

    def test_paid_at_null(self):
        payment = self.payment
        self.assertIsNone(payment.paid_at)
        payment.paid_at = timezone.now()
        payment.save()
        self.assertIsNotNone(payment.paid_at)


class LoanModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="customer_id_123",
            status=1,
            score=85.50,
        )
        self.loan = Loan.objects.create(
            external_id="loan_id_123",
            amount=5000.00,
            status=1,
            contract_version="v1.0",
            customer_id=self.customer,
            outstanding=5000.00,
        )

    def test_loan_creation(self):
        loan = self.loan
        self.assertTrue(isinstance(loan, Loan))
        self.assertEqual(loan.external_id, "loan_id_123")
        self.assertEqual(loan.amount, 5000.00)
        self.assertEqual(loan.status, 1)
        self.assertEqual(loan.contract_version, "v1.0")
        self.assertEqual(loan.customer_id, self.customer)
        self.assertEqual(loan.outstanding, 5000.00)

    def test_created_at_auto_now_add(self):
        loan = self.loan
        self.assertIsNotNone(loan.created_at)
        self.assertTrue((timezone.now() - loan.created_at).total_seconds() < 10)

    def test_updated_at_auto_now(self):
        loan = self.loan
        original_updated_at = loan.updated_at
        loan.status = 2
        loan.save()
        self.assertNotEqual(loan.updated_at, original_updated_at)

    def test_external_id_unique(self):
        with self.assertRaises(Exception):
            Loan.objects.create(
                external_id="loan_id_123",  # Duplicate external_id
                amount=6000.00,
                status=2,
                contract_version="v2.0",
                customer_id=self.customer,
                outstanding=6000.00,
            )

    def test_taken_at_auto_now(self):
        loan = self.loan
        self.assertIsNotNone(loan.taken_at)
        self.assertTrue((timezone.now() - loan.taken_at).total_seconds() < 10)

    def test_maximum_payment_date_auto_now(self):
        loan = self.loan
        self.assertIsNotNone(loan.maximum_payment_date)
        self.assertTrue(
            (timezone.now() - loan.maximum_payment_date).total_seconds() < 10
        )


class PaymentDetailModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="customer_id_123",
            status=1,
            score=85.50,
        )
        self.loan = Loan.objects.create(
            external_id="loan_id_123",
            amount=5000.00,
            status=1,
            contract_version="v1.0",
            customer_id=self.customer,
            outstanding=5000.00,
        )
        self.payment = Payment.objects.create(
            external_id="payment_id_123",
            total_amount=100.1234567890,
            status=1,
            customer_id=self.customer,
        )
        self.payment_detail = PaymentDetail.objects.create(
            amount=100.1234567890,
            loand_id=self.loan,
            payment_id=self.payment,
        )

    def test_payment_detail_creation(self):
        payment_detail = self.payment_detail
        self.assertTrue(isinstance(payment_detail, PaymentDetail))
        self.assertEqual(payment_detail.amount, 100.1234567890)
        self.assertEqual(payment_detail.loand_id, self.loan)
        self.assertEqual(payment_detail.payment_id, self.payment)

    def test_created_at_auto_now_add(self):
        payment_detail = self.payment_detail
        self.assertIsNotNone(payment_detail.created_at)
        self.assertTrue(
            (timezone.now() - payment_detail.created_at).total_seconds() < 10
        )

    def test_updated_at_auto_now(self):
        payment_detail = self.payment_detail
        original_updated_at = payment_detail.updated_at
        payment_detail.amount = 200.1234567890
        payment_detail.save()
        self.assertNotEqual(payment_detail.updated_at, original_updated_at)


class CustomerLogicTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer", score=Decimal("1000.00"), status=2
        )
        Loan.objects.create(
            customer_id=self.customer,
            amount=Decimal("500.00"),
            status=1,
            outstanding=Decimal("500.00"),
        )

    def test_get_total_debt(self):
        total_debt = get_total_debt(self.customer.id)
        self.assertEqual(total_debt, Decimal("500.00"))

    def test_get_available_amount(self):
        available_amount = get_available_amount(self.customer)
        self.assertEqual(available_amount, Decimal("500.00"))


class LoanLogicTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer", score=Decimal("1000.00"), status=2
        )

    def test_create_loan(self):
        loan_data = {
            "customer_external_id": "test_customer",
            "amount": Decimal("200.00"),
        }
        created_loan = create_loan(loan_data)

        # Check if loan object is created
        self.assertIsInstance(created_loan, Loan)

        # Check if loan amount is correct
        self.assertEqual(created_loan.amount, Decimal("200.00"))

    def test_create_loan_exceeding_score(self):
        loan_data = {
            "customer_external_id": "test_customer",
            "amount": Decimal("1200.00"),
        }
        with self.assertRaises(ValidationError) as cm:
            create_loan(loan_data)
        error_detail = cm.exception.detail[0]
        self.assertEqual(
            str(error_detail), "Total outstanding loans exceed customer's credit score"
        )

    def test_create_loan_nonexistent_customer(self):
        loan_data = {
            "customer_external_id": "nonexistent_customer",
            "amount": Decimal("200.00"),
        }
        with self.assertRaises(ValidationError) as cm:
            create_loan(loan_data)
        error_detail = cm.exception.detail[0]
        self.assertEqual(str(error_detail), "Customer not found")


class PaymentLogicTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer", score=Decimal("1000.00"), status=2
        )
        self.loan = Loan.objects.create(
            customer_id=self.customer,
            amount=Decimal("500.00"),
            status=1,
            outstanding=Decimal("500.00"),
        )

    def test_create_payment(self):
        payment_data = {
            "customer_external_id": "test_customer",
            "total_amount": Decimal("300.00"),
        }
        created_payment = create_payment(payment_data)

        # Check if payment object is created
        self.assertIsInstance(created_payment, Payment)

        # Check if payment details are created
        payment_details = PaymentDetail.objects.filter(payment_id=created_payment)
        self.assertTrue(payment_details.exists())

        # Check if loan outstanding is updated correctly
        updated_loan = Loan.objects.get(pk=self.loan.pk)
        self.assertEqual(updated_loan.outstanding, Decimal("200.00"))

    def test_create_payment_exceeding_outstanding(self):
        payment_data = {
            "customer_external_id": "test_customer",
            "total_amount": Decimal("600.00"),
        }
        with self.assertRaises(ValidationError) as cm:
            create_payment(payment_data)
        error_detail = cm.exception.detail[0]
        self.assertEqual(
            str(error_detail), "Total payment amount exceeds outstanding loan values"
        )

    def test_create_payment_no_outstanding_loans(self):
        self.loan.outstanding = Decimal("0.00")
        self.loan.save()
        payment_data = {
            "customer_external_id": "test_customer",
            "total_amount": Decimal("100.00"),
        }
        with self.assertRaises(ValidationError) as cm:
            create_payment(payment_data)
        error_detail = cm.exception.detail[0]
        self.assertEqual(
            str(error_detail), "Total payment amount exceeds outstanding loan values"
        )
