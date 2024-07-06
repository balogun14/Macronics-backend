from django.db import models
from users.models import User

# Create your models here.


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, related_name="vendor", on_delete=models.CASCADE
    )
    cac_number = models.CharField(max_length=100)
    business_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="category")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="brand")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
    def __str__(self):
        return self.name
