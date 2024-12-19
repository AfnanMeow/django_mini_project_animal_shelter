from django.shortcuts import render
from .models import Pet
from django.db.models import Q

# Create your views here.


def index(request):
    # Retrieve search criteria from the form
    serialno_query = request.GET.get('serial_no', '')
    name_query = request.GET.get('name', '')
    type_query = request.GET.get('type', '')
    estCost_query = request.GET.get('estimated_cost', '')
    # Fetch all animals from the database if Queries are empty
    if serialno_query and name_query and type_query and estCost_query == None :
        pets = Pet.objects.all()
    
        # Pass the fetched pets to the template
        return render(request, "index.html", {"pets": pets})
    
    else :
        query = "SELECT * FROM shelterapp_pet WHERE 1=1"  # Start with a base query
        params = []
        pets = Pet.objects.all() #by default it will show all animals, naile last e pets reffered before assigned dekhai
        if serialno_query:
            #pets = pets.filter(serial_no__icontains=serialno_query)
            query += " AND serial_no LIKE %s"
            params.append(f"%{serialno_query}%")

        if name_query:
            #pets = pets.filter(name__icontains=name_query)
            query += " AND name LIKE %s"
            params.append(f"%{name_query}%")
        if type_query:
            #pets = pets.filter(type__icontains=type_query)
            query += " AND type LIKE %s"
            params.append(f"%{type_query}%")
        if estCost_query:
            try:
                budget = int(estCost_query)
                #pets = pets.filter(estimated_cost__lte=budget)
                query += " AND estimated_cost <= %s"
                params.append(budget)
                
            except ValueError:
                #pets = pets.none()  # Invalid budget input
                query += " AND 1=0"
                
        pets = Pet.objects.raw(query, params)


        # Render the results in the template
        return render(request, "index.html", {
            "pets": pets,
            "serialno_query": serialno_query,
            "name_query": name_query,
            "type_query": type_query,
            "estCost_query": estCost_query,})