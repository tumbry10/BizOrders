from django.db import models
from accounts.models import CustomUser
from products.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Sum


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('READY', 'Ready'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 3}, related_name='customer_orders')
    sales_rep = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 2}, related_name='sales_orders')
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Auto-set price from product if not provided
        if self.product and not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# -------------------------
# Signals to auto-update Order total_amount
# -------------------------
@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total = order.items.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    order.total_amount = total
    order.save()
