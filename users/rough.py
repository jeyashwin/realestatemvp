import pandas as pd
data = pd.read_csv("/home/pcuser/Desktop/real/new_app/realestatemvp/ny_data.csv")

wanted_columns = ["PROPERTY TYPE","ADDRESS","CITY","ZIP OR POSTAL CODE","PRICE","BEDS","BATHS","LOCATION","SQUARE FEET"]
jd = data[data["CITY"] == "New York"][wanted_columns][:10].reset_index().to_dict()
import json

json.dumps(jd)


import uuid

uuid.uuid4().hex[:8]