from django.shortcuts import render
from .models import Pet

# Create your views here.


def index(request):
    # Fetch all animals from the database
    pets = Pet.objects.all()
    
    # Pass the fetched pets to the template
    return render(request, "index.html", {"pets": pets})