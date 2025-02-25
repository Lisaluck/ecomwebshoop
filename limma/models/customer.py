# models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)  # Allow NULL values
    phone = models.CharField(max_length=50, unique=True)  # Ensure phone numbers are unique

    def __str__(self):
        return self.name if self.name else f"Customer {self.phone}"