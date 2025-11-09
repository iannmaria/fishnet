

# Create your models here.
from django.db import models
from users.models import CustomUser


class FishermanProfile(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, default='')
    license_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    address = models.TextField(blank=True, default='')
    id_proof = models.ImageField(upload_to='fisherman_documents/', blank=True, null=True)
    license_document = models.ImageField(upload_to='fisherman_documents/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    registration_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}"


class DailyCatch(models.Model):
    fisherman = models.ForeignKey(FishermanProfile, on_delete=models.CASCADE)
    fish_type = models.CharField(max_length=100)
    quantity = models.FloatField()
    price_per_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.fish_type} by {self.fisherman.user.username} ({self.quantity} kg)"


class Complaint(models.Model):
    fisherman = models.ForeignKey(FishermanProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    admin_reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Complaint: {self.title}"
