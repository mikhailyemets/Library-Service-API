import stripe
from django.conf import settings
from django.urls import reverse


def create_stripe_session(request, instance):
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

    success_url = request.build_absolute_uri(
        reverse(
            "payments:success_payment",
            kwargs={
                "pk": instance.pk
            }
        )
    )

    cancel_url = request.build_absolute_uri(
        reverse(
            "payments:cancel_payment"
        )
    )

    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
