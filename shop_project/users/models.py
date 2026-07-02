from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length = 20,
        blank=True
    )
    address = models.TextField( blank=True)
    def __str__(self):
        return self.user.username
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'product')
    def __str__(self):
        return f'{self.username} - {self.product.name}'