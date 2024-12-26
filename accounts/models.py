from django.db import models
from django.contrib.auth.models import AbstractUser

# USER Model (Base for Donor, Adopter, Authority)
class User(AbstractUser):
    #nid = models.CharField(max_length=20, unique=True)
    nid = models.BigIntegerField(unique = True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()
    street = models.CharField(max_length=50)
    # old field
    # house_no = models.CharField(max_length=50)
    
    # renamed field
    house = models.CharField(max_length=50)
   #street_no = models.CharField(max_length=50)
    #house_no = models.CharField(max_length=50)    
    postal_code = models.IntegerField()
    police_station = models.CharField(max_length=100)

    #REQUIRED_FIELDS = ['email', 'phone', 'nid']

    def __str__(self):
        return self.name

# DONOR Model
class Donor(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='donor')
    
    #user = models.ForeignKey(User, to_field='nid', on_delete=models.CASCADE, related_name='donor', unique = True)
    #donation_date = models.DateField()
    #donation_time = models.TimeField()

    def __str__(self):
        return f"Donor: {self.user.name} donated on"  #we need to bring donation date from pet table

# ADOPTER Model
class Adopter(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='adopter')
    
    #user = models.ForeignKey(User, to_field='nid', on_delete=models.CASCADE, related_name='adopter',  unique = True)
    #adoption_date = models.DateField(null=True, blank=True)
    #adoption_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Adopter: {self.user.name}" #we need to bring adoption date from pet table

# AUTHORITY Model (Specific Role for Users)
class Authority(models.Model):
    user = models.OneToOneField(User, to_field='nid', on_delete=models.CASCADE, related_name='authority')
    role = models.CharField(max_length=100)
    #user = models.ForeignKey(User, to_field='nid', on_delete=models.CASCADE, related_name='authority',  unique = True)
    #role = models.CharField(max_length=100)  # e.g., Admin, Manager, Caretaker

    def __str__(self):
        return f"{self.user.name} - {self.role}"