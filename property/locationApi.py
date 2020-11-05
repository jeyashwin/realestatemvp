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
