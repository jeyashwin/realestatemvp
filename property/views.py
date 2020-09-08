from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from .models import PROPERTY,MEDIA
from users.models import LANDLORD
from django.core.files import File
import pymongo
from PIL import Image
import os
import  uuid
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
data = pd.read_csv("ny_data.csv")
data = data.dropna(subset=["CITY"])

class MONGO_CONFS:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["property_data"]
    mycol = mydb["comments"]


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
@csrf_exempt
def view_register(request):
    return render(request, "templates/submit-property.html", {})

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
        add_data = PROPERTY(address = address,city = city,zipcode = zipcode,description = description,property_type = property_type,property_status = property_status,country = country,
                            bedrooms = bedrooms,bathrooms = bathrooms,garage = garage,sqft = sqft,price = price,property_name = property_name,l_id = l,property_id = pid)
        add_data.save()
        get_pid = PROPERTY.objects.get(property_id=pid)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(BASE_DIR,"media/property")
        os.mkdir(base_dir + "/" + pid)
        if "property-images" in request.FILES:
            print(request.FILES['property-images'],"dict")
            im = Image.open(request.FILES["property-images"])
            full_path = base_dir+"/"+pid+"/"+request.FILES["property-images"].name
            im.save(full_path)
            add_image = MEDIA(media_path = full_path,media_type = "image",p_id = get_pid,s_id = "1234",likes = 0,dislikes = 0)
            add_image.save()
        # get_property = PROPERTY.objects.all(l_id = l)
        return render(request,"templates/properties.html",{"status" : 1})
    else:
        return render(request, "templates/index.html", {"status": 0})

@csrf_exempt
def test_single(request):
    return render(request,"templates/single-property.html",{})

@csrf_exempt
def add_comment(request):
    print(request.POST["property-comment"],dict(request.POST))
    comments = MONGO_CONFS.mycol
    comments.insert_one({"user_id": request.POST['user_id'],
                         "property_id": request.POST['property_id'],
                         "comment": request.POST['property-comment'], "sequence": 0})
    return render(request,"templates/single-property.html",{})

















