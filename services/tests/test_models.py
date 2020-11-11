from django.test import TestCase
from unittest.mock import patch

from services.models import *

class ServicesModelTests(TestCase):
    """ Test case for all the models in the service app """

    def test_service_model_str(self):
        """ Test the services model string representation"""
        service = Service.objects.create(serviceName='Bed', description="Nice branded and comfort bed",
                    rentCycle='monthly', price=2000)

        self.assertEqual(str(service), service.serviceName)

    def test_service_image_model_str(self):
        """ Test the services Image model string representation"""
        service = Service.objects.create(serviceName='Bed', description="Nice branded and comfort bed",
                    rentCycle='monthly', price=2000)
        image = ServiceImage.objects.create(service=service, image='bed.jpg')

        self.assertEqual(str(image), str(service.id))

    @patch('uuid.uuid4')
    def test_service_image_file_name_uuid(self, mock_uuid):
        """Test that service image is saved in a correct location with unique file name"""
        uuid = 'test-uuid1'
        mock_uuid.return_value = uuid
        file_path = service_image_file_path(None, 'sampleimage.jpg')
        exp_path = f'uploads/services/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)