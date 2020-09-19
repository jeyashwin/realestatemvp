from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.forms import ValidationError

import datetime

from users import models


def sampleUser(email="test@v.com", password="TestPass", first_name="TestName"):
    """Create a sample user"""
    return get_user_model().objects.create(email=email, password=password, first_name=first_name)

class ModelTests(TestCase):

    def test_generate_unique_username_when_new_user_created_without_username(self):
        """Test creating a new user with an automatic unique username."""
        email1 = "test@growarnappdev.com"
        password1 = "Testpass123"
        first_name1 = " Aravind Sunda ram "

        email2 = "test@growarnappdev.com"
        password2 = "Testpass123"
        first_name2 = " Aravind Sundaram"

        user1 = sampleUser(email1, password1, first_name1)
        user2 = sampleUser(email2, password2, first_name2)
        
        self.assertEqual(user1.email, email1)
        self.assertEqual(user2.email, email2)
        self.assertEqual(user1.username, "AravindSundaram")
        self.assertEqual(str(user2.username)[0:-4], "AravindSundaram")
    
    def test_generate_unique_username_when_new_user_created_with_username(self):
        """Test creating a new user with an username."""

        username = "Test1"
        password = "Testpass123"
        first_name = " Test Name"

        user = get_user_model().objects.create_user(username=username, 
                        password=password, first_name=first_name)

        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertTrue(user.check_password(password))

    def test_usertype_model(self):
        """Test the usertype's property, fields and string representation"""
        user1 = sampleUser()
        user2 = sampleUser()

        usertype1 = models.UserType.objects.create(
            user=user1,
            userType="buyer"
        )

        usertype2 = models.UserType.objects.create(
            user=user2,
            userType="seller"
        )

        self.assertEqual(usertype1.buyer, True)
        self.assertEqual(usertype1.landLord, False)
        self.assertEqual(usertype1.is_buyer, True)
        self.assertEqual(usertype1.is_landlord, False)
        self.assertEqual(str(usertype1.user.username), user1.username)

        self.assertEqual(usertype2.buyer, False)
        self.assertEqual(usertype2.landLord, True)
        self.assertEqual(usertype2.is_buyer, False)
        self.assertEqual(usertype2.is_landlord, True)
        self.assertEqual(str(usertype2.user.username), user2.username)

    def test_userbuyer_with_valid_input_model(self):
        """Test the userbuyer string representaion with valid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="buyer"
        )

        userbuyer = models.UserBuyer.objects.create(
            user=usertype,
            dateOfBirth=str(datetime.date(2020, 7, 10))
        )

        self.assertEqual(str(userbuyer.pk), str(userbuyer))
        self.assertEqual(userbuyer.dateOfBirth, "2020-07-10")
    
    def test_userbuyer_with_invalid_input_model(self):
        """Test the userbuyer with invalid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="seller"
        )

        userbuyer = models.UserBuyer.objects.create(
            user=usertype,
            dateOfBirth=str(datetime.date(2020, 7, 10))
        )

        self.assertRaises(ValidationError, userbuyer.clean)

    def test_userlandlord_with_valid_input_model(self):
        """Test the userlandlord string representaion with valid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="seller"
        )

        userlandlord = models.UserLandLord.objects.create(
            user=usertype,
            dateOfBirth=str(datetime.date(2020, 7, 10))
        )

        self.assertEqual(str(userlandlord.pk), str(userlandlord))
        self.assertEqual(userlandlord.dateOfBirth, "2020-07-10")

    def test_userlandlord_with_invalid_input_model(self):
        """Test the userlandlord with invalid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="buyer"
        )

        userlandlord = models.UserLandLord.objects.create(
            user=usertype,
            dateOfBirth=str(datetime.date(2020, 7, 10))
        )

        self.assertRaises(ValidationError, userlandlord.clean)

    @patch('uuid.uuid4')
    def test_profile_image_file_name_uuid(self, mock_uuid):
        """Test that profile image is saved in a correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.profile_image_file_path(None, 'sampleimage.jpg')
        exp_path = f'uploads/profilePicture/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)