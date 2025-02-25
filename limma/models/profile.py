from django.db import models
from .customer import Customer

class Profile(models.Model):
    name = models.OneToOneField(Customer, on_delete=models.CASCADE)  # Link to Customer, not User
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"