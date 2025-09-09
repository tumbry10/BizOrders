from django.db import models
from accounts.models import CustomUser
from django.db.models import Max

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    sku = models.CharField(max_length=50, unique=True, editable=False)
    description = models.TextField(blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-generate SKU if not provided
        if not self.sku and self.name:
            prefix = self.name[:3].upper()

            # Get the last SKU with the same prefix
            last_sku = Product.objects.filter(sku__startswith=prefix).aggregate(
                max_sku=Max("sku")
            )["max_sku"]

            if last_sku:
                # Extract numeric part
                last_number = int(last_sku[len(prefix):])
                new_number = last_number + 1
            else:
                new_number = 1

            self.sku = f"{prefix}{new_number:06d}"
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
