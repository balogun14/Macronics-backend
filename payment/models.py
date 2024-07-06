from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.models import Order


class Payment(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, _("pending")),
        (COMPLETED, _("completed")),
        (FAILED, _("failed")),
    )

    # Payment options
  
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"

    PAYMENT_METHOD = (
        (CASH, "Cash"),
        (CARD, "Card"),
        (TRANSFER, "Transfer"),
    )

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_option = models.CharField(max_length=10, choices=PAYMENT_METHOD)
    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.order.buyer.get_full_name()