from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from json import loads
from .models import CustomUser, GolfCourse

# Create your views here.


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        golf_role = request.POST["golf_role"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "turf/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, golf_role=golf_role, username=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "turf/register.html", {
                "message": "User with the entered email already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, 'turf/register.html')


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "turf/login.html", {
                "message": "Invalid email and/or password."
            })
    return render(request, 'turf/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required(login_url='/login/')
def index(request):
    return render(request, 'turf/index.html')


@login_required(login_url='/login/')
@csrf_exempt
def golf_courses(request):
    if request.method == "GET":
        try:
            user = request.user
            golfcourse = GolfCourse.objects.all()
            golf_course_list = []
            for i in golfcourse:
                a = {'id': i.id, 'name': i.name,'address': i.address,'email': i.email,'website': i.website,
                     'description': i.description,'par': i.par,'rating': i.rating,'spatial_extent': i.spatial_extent}
                golf_course_list.append(a)
            return JsonResponse({"status": 0, "notes": golf_course_list})

        except:
            return JsonResponse({"status": 1})
    try:
        golfcourse = loads(request.body)
        title = golfcourse["name"]
        address = golfcourse["address"]
        email = golfcourse["email"]
        website = golfcourse["website"]
        description = golfcourse["description"]
        par = golfcourse["par"]
        rating = golfcourse["rating"]
        spatial_extent = golfcourse["spatial_extent"]
        user = request.user
        course_object= GolfCourse.objects.create(user=user, name=title, address=address, email=email
                                               , website=website, description=description, par=par, rating=rating,
                                               spatial_extent=spatial_extent)
        course_object.save()
        return JsonResponse({"status": 0})
    except:
        return JsonResponse({"status": 1})

