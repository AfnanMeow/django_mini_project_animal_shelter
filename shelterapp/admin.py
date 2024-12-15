from django.contrib import admin
from .models import Pet #creating a add Animal page for the Admins

# Register your models here.
admin.site.register(Pet)