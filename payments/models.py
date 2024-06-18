from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from telegram_bot.bot import send_telegram_message


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'

    class Type(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        FINE = 'FINE', 'Fine'

    borrowing = models.OneToOneField('borrowings.Borrowing',
                                     on_delete=models.CASCADE,
                                     related_name='payment')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PAYMENT)
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(auto_now=True)


@receiver(pre_save, sender=Payment)
def check_payment_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = Payment.objects.get(pk=instance.pk)
        if (previous_instance.status != instance.status
                and instance.status == Payment.Status.PAID):
            instance.notify_payment_completed = True


@receiver(post_save, sender=Payment)
def send_telegram_notification_payment(sender, instance, created, **kwargs):
    if created:
        payment_info = (
            f"ID: {instance.id}, "
            f"Borrowing ID: {instance.borrowing.id}, "
            f"Status: {instance.get_status_display()}, "
            f"Type: {instance.get_type_display()}, "
            f"Money to Pay: {instance.money_to_pay}, "
        )
        message = f"New Payment: {payment_info}"
        send_telegram_message(message)
    elif getattr(instance, 'notify_payment_completed', False):
        payment_info = (
            f"ID: {instance.id}, "
            f"Borrowing ID: {instance.borrowing.id}, "
            f"Status: {instance.get_status_display()}, "
            f"Type: {instance.get_type_display()}, "
            f"Money to Pay: {instance.money_to_pay}, "
        )
        message = f"Payment Paid: {payment_info}"
        send_telegram_message(message)
