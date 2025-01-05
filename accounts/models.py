from django.db import models
from django.contrib.auth.models import AbstractUser

# USER Model (Base for Donor, Adopter, Authority)
class User(AbstractUser):
    nid = models.BigIntegerField(unique = True)
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()
    street = models.CharField(max_length=250)
    house = models.CharField(max_length=250)  
    postal_code = models.IntegerField()
    police_station = models.CharField(max_length=200)
    def __str__(self):
        return self.name

# DONOR Model
class Donor(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='donor')
    def __str__(self):
        return f"Donor: {self.user.name} donated"

# ADOPTER Model
class Adopter(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='adopter')
    def __str__(self):
        return f"Adopter: {self.user.first_name} {self.user.last_name}"

# AUTHORITY Model
class Authority(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='authority')
    role = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user.name} - {self.role}"