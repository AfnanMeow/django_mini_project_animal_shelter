
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect  #sudhu get_object jani kmne use kore ??
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Pet
#from django.db.models import Q


# Create your views here.
def home(request):

    return render (request, "index.html")

def index(request):
    # Retrieve search criteria from the form
    serialno_query = request.GET.get('serial_no', '')
    name_query = request.GET.get('name', '')
    type_query = request.GET.get('type', '')
    estCost_query = request.GET.get('estimated_cost', '')
    status_query = request.GET.get('status', '')
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
        
        if status_query:
            # Add condition for status filter
            query += " AND status = %s"
            params.append(status_query)
                
        pets = Pet.objects.raw(query, params)


        # Render the results in the template
        return render(request, "index.html", {
            "pets": pets,
            "serialno_query": serialno_query,
            "name_query": name_query,
            "type_query": type_query,
            "estCost_query": estCost_query,
            "status_query": status_query,
            })
    


#now we're making history the very first time by sending request with a value

def show_pet_details(request, serial_no):
    pet = get_object_or_404(Pet, serial_no=serial_no)
    return render(request, 'show_pet_details.html', {'pet': pet})




# Adoption view
@login_required
@csrf_exempt
def adopt_pet(request, serial_no):
    if request.method == "POST":
        try:
            adopter_nid = request.user.nid  # Assuming the current user has a `nid` field
            #print(adopter_nid, "whattttttttt !!!!")
            #all these Drama for that foreign key constraint, wasted 2 hours straight
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO accounts_adopter (user_id) 
                    VALUES (%s)
                """, [adopter_nid])
            # Update the Pet record in the database using raw SQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE shelterapp_pet
                    SET adopter_nid_id = %s, adoption_date = CURRENT_DATE, adoption_time = CURRENT_TIME, status = "Adopted"
                    WHERE serial_no = %s AND adopter_nid_id IS NULL
                """, [adopter_nid, serial_no])

            # Check if the pet was successfully updated
            if cursor.rowcount > 0:
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Pet not available for adoption."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})

