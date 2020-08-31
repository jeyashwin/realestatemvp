from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from .models import PROPERTY
from users.models import LANDLORD
import  uuid
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
data = pd.read_csv("ny_data.csv")
data = data.dropna(subset=["CITY"])

def decoder(request,name):
    if request.method == "GET":
        print(name,"REQUEST")
        # print(request.name,"REQ NAME")

def search(request,text):
    print(text,"TEXT")
    wanted_columns = ["PROPERTY TYPE","ADDRESS","CITY","ZIP OR POSTAL CODE","PRICE","BEDS","BATHS","LOCATION","SQUARE FEET"]
    if isinstance(text,int):
        return data[data["ZIP OR POSTAL CODE"] == text][wanted_columns].to_dict()
    if text.lower() in [i.lower() for i in data['CITY'].unique()]:
        exact_txt = [val for val in  list(data['CITY'].unique()) if val.lower() == text]
        return JsonResponse(data[data["CITY"] == exact_txt[0]].to_dict())
    else:
        return JsonResponse({"error":0})

def homepage(request):
    if request.method == "GET":
        return render(request,"templates/index.html",{})
    else:
        return JsonResponse({"Error" : 0})

def view_register(request):
    return render(request, "templates/landlord/db-add-listing.html", {})

@csrf_exempt
def register_property(request):
    if request.method == "POST":
        pid = uuid.uuid4().hex[:8]
        l_id = "79660c01"
        address = request.POST["property-address"]
        city = request.POST["property-city"]
        zipcode = request.POST["property-zipcode"]
        description = request.POST["property-description"]
        # property_updates = request.POST["property_updates"]
        bedrooms = request.POST["property-bedrooms"]
        bathrooms = request.POST["property-bathrooms"]
        garage = request.POST["property-garages"]
        sqft = request.POST["property-sqft"]
        # lot_size = request.POST["property-lot_size"]
        price = request.POST["property-price"]
        property_name = request.POST["property-title"]
        country = request.POST["property-country"]
        # state = request.POST["property-state"]
        property_type = request.POST["property-type"]
        property_status = request.POST["property-status"]
        l = LANDLORD.objects.get(l_id = l_id)
        print(l)

        add_data = PROPERTY(address = address,city = city,zipcode = zipcode,description = description,property_type = property_type,property_status = property_status,country = country,
                            bedrooms = bedrooms,bathrooms = bathrooms,garage = garage,sqft = sqft,price = price,property_name = property_name,l_id = l,property_id = pid)
        add_data.save()
        # get_property = PROPERTY.objects.all(l_id = l)
        return render(request,"templates/landlord/db-my-listing.html",{"status" : 1})
    else:
        return render(request, "templates/index.html", {"status": 0})

