from django.db import models

class Product(models.Model):
    Store=models.CharField(max_length=200)
    ProductName = models.CharField(max_length=200)
    ProductLink = models.URLField()
    ProductImageUrl = models.URLField()
    ProductBrand = models.CharField(max_length=200)
    ProductRating = models.CharField(max_length=200)
    ProductReviews = models.CharField(max_length=200)
    ProductPrice = models.CharField(max_length=200)


    # Add other fields if necessary