from django.db import models
from catalog.models import Product
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length = 150)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'Order #{self.id}'
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        related_name='items',
        on_delete=models.CASCADE
    )
    product=models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity

# Create your models here.
