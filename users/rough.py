import pandas as pd
data = pd.read_csv("/home/pcuser/Desktop/real/new_app/realestatemvp/ny_data.csv")

wanted_columns = ["PROPERTY TYPE","ADDRESS","CITY","ZIP OR POSTAL CODE","PRICE","BEDS","BATHS","LOCATION","SQUARE FEET"]
jd = data[data["CITY"] == "New York"][wanted_columns][:10].reset_index().to_dict()
import json

json.dumps(jd)


import uuid

uuid.uuid4().hex[:8]
from PIL import Image

# open method used to open different extension image file
im = Image.open("/home/pcuser/Documents/prudent/images/1. January 2019 -page-002.jpg")

# This method will show image in any image viewer
im.show()
im.save("/home/pcuser/Documents/prudent/images/added.jpg")


import os
os.getcwd()
os.mkdir('/home/pcuser/Desktop/real'+"/test")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["property_data"]
mycol = mydb["comments"]
ins = mycol.insert_one({"user_id" : 123,"property_id" : 12345,"comment" : "Property looks pretty good","sequence" :0})
print(ins.inserted_ids)
sequenceNextValue("sequence")
for x in mycol.find():
  print(x)













