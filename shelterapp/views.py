
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect  #sudhu get_object jani kmne use kore ??
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import  Pet, Vet, Vet_Visit, CareTaker
from accounts.models import User 
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import os
from django.conf import settings


# Create your views here.
def home(request):
    return render (request, "index.html")

def index(request):
    serialno_query = request.GET.get('serial_no', '')
    name_query = request.GET.get('name', '')
    type_query = request.GET.get('type', '')
    estCost_query = request.GET.get('estimated_cost', '')
    status_query = request.GET.get('status', '')
    if serialno_query and name_query and type_query and estCost_query == None :
        pets = Pet.objects.all()
        return render(request, "index.html", {"pets": pets})
    else :
        query = "SELECT * FROM shelterapp_pet WHERE 1=1"  # Start with a base query
        params = []
        pets = Pet.objects.all()
        if serialno_query:
            query += " AND serial_no LIKE %s"
            params.append(f"%{serialno_query}%")
        if name_query:
            query += " AND name LIKE %s"
            params.append(f"%{name_query}%")
        if type_query:
            query += " AND type LIKE %s"
            params.append(f"%{type_query}%")
        if estCost_query:
            try:
                budget = int(estCost_query)
                query += " AND estimated_cost <= %s"
                params.append(budget)
            except ValueError:
                query += " AND 1=0"
        if status_query:
            query += " AND status = %s"
            params.append(status_query)
        pets = Pet.objects.raw(query, params)
        return render(request, "index.html", {
            "pets": pets,
            "serialno_query": serialno_query,
            "name_query": name_query,
            "type_query": type_query,
            "estCost_query": estCost_query,
            "status_query": status_query,
            })

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
    # First, check if the value already exists in the table
                cursor.execute("""
                    SELECT COUNT(*) FROM accounts_adopter WHERE user_id = %s
                    """, [adopter_nid])
    
                count = cursor.fetchone()[0]  # Fetch the count from the result
    
                if count == 0:  # Only insert if the value doesn't already exist
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


##Disaster starts from here
@login_required
@csrf_exempt
def wanna_donate(request):
    if request.method == "POST":
        serial_no = request.POST.get("serial_no")
        name = request.POST.get("name")
        pet_type = request.POST.get("type")
        description = request.POST.get("description")
        img = request.FILES.get("image")  # Handle file upload
        
        if not (serial_no and name and pet_type and description and img):
            messages.error(request, "All fields are required!")
            return redirect("wanna_donate")
        
        try:
            # Define the path to save the image
            pet_folder = os.path.join(settings.MEDIA_ROOT, "pets")
            os.makedirs(pet_folder, exist_ok=True)  # Ensure the directory exists

            # Save the image file
            img_path = os.path.join(pet_folder, img.name)
            print("wtffffffff"+ str(img_path))
            with open(img_path, "wb") as f:
                for chunk in img.chunks():
                    f.write(chunk)

             # Store relative path in the database
            db_img_path = f"pets/{img.name}"

            with connection.cursor() as cursor:
    # First, check if the value already exists in the table
                cursor.execute("""
                    SELECT COUNT(*) FROM accounts_donor WHERE user_id = %s
                    """, [request.user.nid])
    
                count = cursor.fetchone()[0]  # Fetch the count from the result
    
                if count == 0:  # Only insert if the value doesn't already exist
                    cursor.execute("""
                        INSERT INTO accounts_donor (user_id) 
                        VALUES (%s)
                        """, [request.user.nid])
            # Execute raw SQL query
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO shelterapp_pet (
                        serial_no, name, img, type, description, estimated_cost, status, 
                        donation_date, donation_time, adoption_date, adoption_time, donor_nid_id, adopter_nid_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME, NULL, NULL, %s, NULL)
                """, [
                    serial_no, name, db_img_path, pet_type, description, 10, "Available", request.user.nid
                ])
            
            messages.success(request, "Pet donated successfully!")
            return redirect("donated_pets")  # Redirect to a success page or refresh the form
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            print(str(e))
            return redirect("wanna_donate")
    else:

        return render(request, "wanna_donate.html")


@login_required
@csrf_exempt
def donated_pets(request):
    pets = Pet.objects.all()
    pets = Pet.objects.raw("Select * From shelterapp_pet Where donor_nid_id Like %s", [request.user.nid])


    return render(request, "donated_pets.html", {"pets" : pets})


@login_required
@csrf_exempt
def adopted_pets(request):
    pets = Pet.objects.all()
    pets = Pet.objects.raw("Select * From shelterapp_pet Where adopter_nid_id Like %s", [request.user.nid])


    return render(request, "adopted_pets.html", {"pets" : pets})


@login_required
@csrf_exempt
def authority_view(request):
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
        return render(request, "authority_view.html", {
            "pets": pets,
            "serialno_query": serialno_query,
            "name_query": name_query,
            "type_query": type_query,
            "estCost_query": estCost_query,
            "status_query": status_query,
            })


@login_required
@csrf_exempt
def all_users(request):

    users = User.objects.all()

    return render(request, "all_users.html", {"users":users})

@login_required
@csrf_exempt
def vet_visit(request):
    vets = Vet.objects.all()
    vets_visits = Vet_Visit.objects.all()
    caretakers = CareTaker.objects.all()

    return render(request, "vet_visit.html")