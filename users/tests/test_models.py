from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.forms import ValidationError

from users import models


def sampleUser(username="TestUser", password="TestPass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(username=username, password=password)

class ModelTests(TestCase):

    def test_usertype_model(self):
        """Test the usertype's property, fields and string representation"""
        user1 = sampleUser()
        user2 = sampleUser(username="UserTest")

        usertype1 = models.UserType.objects.create(
            user=user1,
            userType="student"
        )

        usertype2 = models.UserType.objects.create(
            user=user2,
            userType="seller"
        )

        self.assertTrue(usertype1.student)
        self.assertFalse(usertype1.landLord)
        self.assertTrue(usertype1.is_student)
        self.assertFalse(usertype1.is_landlord)
        self.assertEqual(usertype1.user.username, user1.username)

        self.assertFalse(usertype2.student)
        self.assertTrue(usertype2.landLord)
        self.assertFalse(usertype2.is_student)
        self.assertTrue(usertype2.is_landlord)
        self.assertEqual(usertype2.user.username, user2.username)
    
    def test_interest_str(self):
        """Test the interest string representation"""
        interest = models.Interest.objects.create(
            interest="Developer"
        )

        self.assertEqual(str(interest), interest.interest)

    def test_userstudent_with_valid_input_model(self):
        """Test the userStudent string representaion with valid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="student"
        )
        interest1 = models.Interest.objects.create(
            interest="Developer"
        )
        interest2 = models.Interest.objects.create(
            interest="Sports"
        )

        userstudent = models.UserStudent.objects.create(
            user=usertype,
            phone="+12312312312",
            university="safsf afsd",
            classYear=2020,
            bio="asfjlk asfa",
            profilePicture="1.jpeg",
            fbLink="https://www.facebook.com/",
            snapLink="https://www.snapchat.com/",
            instaLink="https://www.instagram.com/",
            redditLink="https://www.reddit.com/",
        )
        userstudent.interests.set([interest1, interest2])

        self.assertEqual(str(userstudent), usertype.user.username)
        self.assertEqual(userstudent.interests.get(interest=interest1), interest1)
        self.assertEqual(userstudent.interests.get(interest=interest2), interest2)
        self.assertEqual(userstudent.profilePicture, "1.jpeg")
        self.assertFalse(userstudent.emailVerified)
        self.assertFalse(userstudent.phoneVerified)
    
    def test_userstudent_with_invalid_input_model(self):
        """Test the userstudent with invalid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="seller"
        )

        interest1 = models.Interest.objects.create(
            interest="Developer"
        )
        interest2 = models.Interest.objects.create(
            interest="Sports"
        )
        userstudent = models.UserStudent.objects.create(
            user=usertype,
            phone="+12312312312",
            university="safsf afsd",
            classYear=200,
            bio="asfjlk asfa",
            profilePicture="1.jpeg",
            fbLink="https://www.facebook.com/",
            snapLink="https://www.snapchat.com/",
            instaLink="https://www.instagram.com/",
            redditLink="https://www.reddit.com/",
        )
        userstudent.interests.set([interest1, interest2])

        with self.assertRaises(ValidationError):
            userstudent.full_clean()

        try:
            userstudent.full_clean()
        except ValidationError as e:
            self.assertEqual(dict(e).get("classYear"), ["Minimum year 2010"])
            self.assertEqual(dict(e).get("user"), ["User is not a student!"])

    def test_userlandlord_with_valid_input_model(self):
        """Test the userlandlord string representaion with valid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="seller"
        )

        userlandlord = models.UserLandLord.objects.create(
            user=usertype,
            phone="+232213123123",
            profilePicture="10.jpeg"
        )

        self.assertEqual(str(userlandlord), usertype.user.username)
        self.assertEqual(userlandlord.phone, "+232213123123")
        self.assertFalse(userlandlord.emailVerified)
        self.assertFalse(userlandlord.phoneVerified)
        self.assertEqual(userlandlord.profilePicture, "10.jpeg")

    def test_userlandlord_with_invalid_input_model(self):
        """Test the userlandlord with invalid input"""
        usertype = models.UserType.objects.create(
            user=sampleUser(),
            userType="student"
        )

        userlandlord = models.UserLandLord.objects.create(
            user=usertype,
            phone="+232213123",
            profilePicture="10.jpg"
        )

        with self.assertRaises(ValidationError):
            userlandlord.full_clean()

        try:
            userlandlord.full_clean()
        except ValidationError as e:
            self.assertEqual(dict(e).get("phone"), ["The phone number entered is not valid."])
            self.assertEqual(dict(e).get("user"), ["User is not a Seller!"])

    @patch('uuid.uuid4')
    def test_profile_image_file_name_uuid(self, mock_uuid):
        """Test that profile image is saved in a correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.profile_image_file_path(None, 'sampleimage.jpg')
        exp_path = f'uploads/profilePicture/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
