from django.db import models
from accounts.models import User, Donor, Adopter, Authority

# Create your models here.

#PET Model
class Pet(models.Model):
    serial_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to = "pics")
    type = models.CharField(max_length=50)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default="AVAILABLE")
    donation_date = models.DateField()
    donation_time = models.TimeField()
    adoption_date = models.DateField(null=True, blank=True)
    adoption_time = models.TimeField(null=True, blank=True)
    donor_nid = models.ForeignKey(Donor, to_field='user_id', related_name="donated_pets",unique = False, on_delete=models.CASCADE)
    adopter_nid = models.ForeignKey(Adopter, to_field='user_id', related_name="adopted_pets", on_delete=models.SET_NULL, unique = False, null=True, blank=True)
    def __str__(self):
        return self.name

# VET Model
class Vet(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)
    nid = models.BigIntegerField(unique=True)
    def __str__(self):
        return self.name

# VISIT Model (Pet visits Vet)
class Vet_Visit(models.Model):
    serial_no = models.ForeignKey(Pet, to_field='serial_no', on_delete=models.CASCADE, related_name='visits')
    vet = models.ForeignKey(Vet, to_field='nid', on_delete=models.CASCADE, related_name='vet_visits')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    medicines = models.CharField(max_length=255, default='No medicines prescribed')
    def __str__(self):
        return f"Visit: {self.serial_no.name} to {self.vet.name} on {self.date}"

#CARETAKER model (Authourity cares for pets)
class CareTaker(models.Model):
    pet = models.ForeignKey(Pet, to_field='serial_no', on_delete=models.CASCADE, related_name='care_takers')
    auth_nid = models.ForeignKey(Authority, to_field='user_id', on_delete=models.CASCADE, related_name='cared_pets')
    def __str__(self):
        return f"{self.auth_nid.name} cares for {self.pet.name}"
