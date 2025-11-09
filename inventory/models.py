from django.db import models


class FishCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FishItem(models.Model):
    category = models.ForeignKey(FishCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price_per_kg = models.FloatField()
    stock = models.FloatField()
    image = models.ImageField(upload_to='fish_images/', null=True, blank=True)

    def __str__(self):
        return self.name
