from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from products.models import Products
from users.models import Address

User = get_user_model()


class Order(models.Model):
    PENDING = 'P'
    COMPLETED = 'CO'
    CANCELED = 'CA'

    ORDER_STATUS = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Cancelled'),
    )

    buyer = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default=PENDING)
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        Address,
        related_name="billing_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.buyer.get_full_name()

    @cached_property
    def total_cost(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Products, related_name="product_orders", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.order.buyer.get_full_name()

    @cached_property
    def cost(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.price, 2)

