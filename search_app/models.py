from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.


class CollectableShoe(models.Model):
    RARITY_CHOICES = [
        ("C", "Common"),
        ("U", "Uncommon"),
        ("R", "Rare"),
        ("VR", "Very Rare"),
        ("UR", "Ultra Rare"),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    year_produced = models.PositiveIntegerField()
    collaboration_artist = models.CharField(max_length=100, blank=True, null=True)
    sku_code = models.CharField(max_length=50, unique=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_on_release = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=4, decimal_places=1)
    rarity = models.CharField(max_length=2, choices=RARITY_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.color} (Size: {self.size})"


class ShoeDescription(models.Model):
    shoe = models.OneToOneField(CollectableShoe, on_delete=models.CASCADE)
    description = MDTextField()

    def __str__(self):
        return f"Description for {self.shoe}"
