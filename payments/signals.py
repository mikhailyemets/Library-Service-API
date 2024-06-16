import stripe
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowings.models import Borrowing
from payments.models import Payment


@transaction.atomic
@receiver(post_save, sender=Borrowing, dispatch_uid="create_payment_and_stripe_session")
def create_payment_and_stripe_session(sender, instance, **kwargs):
    days_to_pay = (instance.expected_return_date - instance.borrow_date).days
    money_to_pay = int(instance.book.daily_fee * days_to_pay) * 100
    product_data = {
        'name': instance.book.title,
    }
    price_data = {
        'product_data': product_data,
        'currency': 'usd',
        'unit_amount': money_to_pay,
    }
    line_items = [
        {
            'price_data': price_data,
            'quantity': 1,
        }
    ]
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    Payment.objects.create(
        borrowing=instance,
        session_url=stripe_session.url,
        session_id=stripe_session.id,
        status=Payment.Status.PENDING,
        type=Payment.Type.PAYMENT,
        money_to_pay=money_to_pay
    )
