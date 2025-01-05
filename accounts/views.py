from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from accounts.models import User
from django.db import connection

# Create your views here.

def signup(request) :
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password1 = request.POST["password_1"]
        password2 = request.POST["password_2"]
        email = request.POST["email"]
        nid =  request.POST["nid"]
        phone =  request.POST["phone"]
        street =  request.POST["street"]
        house = request.POST["house"]
        postalcode =  request.POST["postalcode"]
        policestation =  request.POST["policestation"]
        if password1 != password2:
            messages.info(request, "Passwords do not match")
            return redirect("signup")
        if User.objects.filter(username = username).exists():
            messages.info(request, "Username is already taken")
            return redirect("signup")
        if User.objects.filter(email = email).exists():
            messages.info(request, "Email is already registered")
            return redirect("signup")
        user = User.objects.create_user(
            username = username,
            password = password1,
            email = email,
            first_name = first_name,
            last_name = last_name,
            nid = nid,
            phone = phone,
            street = street,
            house = house,
            postal_code = postalcode,
            police_station = policestation
        )
        user.save()
        messages.info(request, "User created successfully. Please log in.")
        return redirect("signin")
    return render(request, "signup.html")
        
def signin(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password1 = request.POST["password_1"]
        user = auth.authenticate(username = username, password = password1)
        if user is not None:
            auth.login(request, user)
            return redirect ("/")
        else:
            messages.info(request, "Wrong Username or Password")
            return render(request, "signin.html")  
    else :
        return render(request, "signin.html")   
    
def logout(request):
    auth.logout(request)
    return redirect ("/")