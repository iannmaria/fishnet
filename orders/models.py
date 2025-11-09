from django.db import models
from users.models import CustomUser
from inventory.models import FishItem


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fish_item = models.ForeignKey(FishItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Cart: {self.user.username} - {self.fish_item.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    fish_item = models.ForeignKey(FishItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()  # Price at time of order
    
    def __str__(self):
        return f"Order #{self.order.id} - {self.fish_item.name} ({self.quantity} kg)"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
