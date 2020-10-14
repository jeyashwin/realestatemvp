from django.test import TestCase
from unittest.mock import patch
from django.http import Http404

from property import utils, models
from property.tests.test_models import sampleProperty
from users.tests.test_views import createStudentUser, createLandlordUser

class PropertyUtilsTests(TestCase):
    """ Test all the utils in Property App"""

    @patch('uuid.uuid4')
    def test_property_image_file_name_uuid(self, mock_uuid):
        """Test that property image is saved in a correct location"""
        propObject = sampleProperty()
        imageInstance = models.PropertyImage.objects.create(propertyKey=propObject, 
                        imageDescription="Bed")
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = utils.unique_file_path_generator(imageInstance, 'sampleimage.jpg')
        exp_path = f'uploads/property/{propObject.pk}/{imageInstance.mediaType}/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)

    @patch('uuid.uuid4')
    def test_property_video_file_name_uuid(self, mock_uuid):
        """Test that property video is saved in a correct location"""
        propObject = sampleProperty()
        videoInstance = models.PropertyVideo.objects.create(propertyKey=propObject, 
                        videoDescription="hall")
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = utils.unique_file_path_generator(videoInstance, 'sampleVideo.mp4')
        exp_path = f'uploads/property/{propObject.pk}/{videoInstance.mediaType}/{uuid}.mp4'

        self.assertEqual(file_path, exp_path)

    def test_unique_slug_generator(self):
        """Test that unique slug is generated correctly"""
        propObject1 = sampleProperty()
        propObject2 = sampleProperty()

        self.assertEqual(propObject1.urlSlug, "new-property-near-lake")
        self.assertNotEqual(propObject2.urlSlug, "new-property-near-lake")

    def test_student_access(self):
        """Test that only student can access"""
        stud = createStudentUser()
        land = createLandlordUser(username="Test")

        self.assertTrue(utils.studentAccessTest(stud))
        with self.assertRaises(Http404):
            utils.studentAccessTest(land)

    def test_landlord_access(self):
        """Test that only landlord can access"""
        stud = createStudentUser()
        land = createLandlordUser(username="Test")

        self.assertTrue(utils.landlordAccessTest(land))
        with self.assertRaises(Http404):
            utils.landlordAccessTest(stud)