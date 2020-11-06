import googlemaps, logging
from django.conf import settings

gmapsClient = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

logging.basicConfig(level=logging.DEBUG, filename='completeApp.log', format='%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# logging.warning('This will get logged to a file')
# logging.debug('This will get logged to a file')
# logging.info('This will get logged to a file')
# logging.error('This will get logged to a file')
# logging.critical('This will get logged to a file')

def get_lat_long_from_address(address):
    """ function to get lat and long based on property address"""
    status = True
    placeId = ""
    locationType = ""
    location = {}
    
    try:
        geocodeResult = gmapsClient.geocode(address=address)
        if geocodeResult:
            geometry = geocodeResult[0].get('geometry', None)
            placeId = geocodeResult[0].get('place_id', None)
            locationType = geometry.get('location_type', None)
            location = geometry.get('location', None)
            if locationType == 'APPROXIMATE':
                logging.warning('Could not fetch exact address for - {}.'.format(address))
                status = False
        else:
            logging.warning('Geocode returned empty for the address - {}.'.format(address))
            status = False
    except Exception as e:
        print(e)
        logging.error('Error occurred when fetching geocode api. Address is - {} and error is - {}'.format(address, e))
        status = False

    return placeId, locationType, location, status

def get_near_by_types(instance=None, types=None, count=1):
    """ function to get nearest location of types around the property"""
    success = True
    nearByName = ""
    locationDict = {}
    placeId = ""
    try:
        nearbyResult = gmapsClient.places_nearby(
            location=(instance.location.y, instance.location.x),
            type=types,
            rank_by="distance"
        )
        requestStatus = nearbyResult.get('status', None)
        if requestStatus == 'OK':
            requestResult = nearbyResult.get('results', None)
            for result in requestResult:
                businessStatus = result.get('business_status', None)
                if businessStatus == 'OPERATIONAL':
                    geometry = result.get('geometry', None)
                    locationDict = geometry.get('location', None)
                    nearByName = result.get('name', None)
                    placeId = result.get('place_id', None)
                    return success, nearByName, locationDict, placeId
        elif requestStatus == 'ZERO_RESULTS':
            logging.warning('Near by api returened empty for Property - {}, '
                        'address - {}, type - {}. So retried {} times.'.format(instance.title, instance.address, types, count))
            if count<3:
                get_near_by_types(instance=instance, types=types, count=count+1)
        else:
            logging.critical('Near by api returened with error of property - {}, address - {} and status - {} for '
                        'type - {}.'.format(instance.title, instance.address, requestStatus, types))
    except Exception as e:
        print(e)
        logging.error('Error occurred when fetching near by types. Property is - {}, '
                        'address is - {} and error is - {}'.format(instance.title, instance.address, e))
        success = False

    return success, nearByName, locationDict, placeId

def get_near_by_text_places(instance=None, place=None, count=1):
    """ function to get nearest location of places text search around the property"""
    success = True
    nearByName = ""
    locationDict = {}
    placeId = ""
    try:
        placesResult = gmapsClient.places(
            place,
            location=(instance.location.y, instance.location.x),
        )
        requestStatus = placesResult.get('status', None)
        if requestStatus == 'OK':
            requestResult = placesResult.get('results', None)
            for result in requestResult:
                businessStatus = result.get('business_status', None)
                if businessStatus == 'OPERATIONAL':
                    geometry = result.get('geometry', None)
                    locationDict = geometry.get('location', None)
                    nearByName = result.get('name', None)
                    placeId = result.get('place_id', None)
                    return success, nearByName, locationDict, placeId
        elif requestStatus == 'ZERO_RESULTS':
            logging.warning('Places api returened empty for Property - {}, '
                        'address - {}, type - {}. So retried {} times.'.format(instance.title, instance.address, place, count))
            if count<3:
                get_near_by_text_places(instance=instance, place=place, count=count+1)
        else:
            logging.critical('Places api returened with error of property - {}, address - {} and status - {} for '
                        'type - {}.'.format(instance.title, instance.address, requestStatus, place))
    except Exception as e:
        print(e)
        logging.error('Error occurred when fetching places text search. Property is - {}, '
                        'address is - {} and error is - {}'.format(instance.title, instance.address, e))
        success = False

    return success, nearByName, locationDict, placeId