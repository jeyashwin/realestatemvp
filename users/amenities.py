import requests, json


api_key = 'AIzaSyBZs3lC3Z72FBlv40cGOi5X6sYlZa9mHE4'
geocode = "https://maps.googleapis.com/maps/api/geocode/json?address="
urlPlaces = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
urlDistance = "https://maps.googleapis.com/maps/api/distancematrix/json?"

def amenities():
    amenitiesHelper("1380 Stony Brook Rd., Stony Brook, NY 11790")

def amenitiesHelper(property):
    amenityList = ["Restaurants in", "Malls in", "Costco in", "Target in", "Walmart in", "Bars in"]
    tempamenities = []

    for i in range(len(amenityList)):
        r = requests.get(urlPlaces + 'query=' + amenityList[i] + property + '&key=' + api_key)
        x = r.json()
        y = x['results']

        if amenityList[i] == "Costco in" or amenityList[i] == "Target in":
            tempamenities.append({'Amenity': y[i]['name'], 'Address': y[i]['formatted_address'],
                                  'Location': y[i]['geometry']['location']})
        elif amenityList[i] == "Walmart in":
            for i in range(1):
                tempamenities.append({'Amenity': y[i]['name'], 'Address': y[i]['formatted_address'],
                                      'Location': y[i]['geometry']['location']})
        else:
            for i in range(3):
                tempamenities.append({'Amenity': y[i]['name'], 'Address': y[i]['formatted_address'],
                                      'Location': y[i]['geometry']['location']})
    for i in range(len(tempamenities)):
         print(tempamenities[i])

    return tempamenities

amenities()