from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status, exceptions

from PIL import Image
import tempfile

from students.serializers import RoommatePostDetailSerializer, RoommatePostSerializer
from students.models import RoommatePost, Preference
from students.tests.test_models import createStudent
from users.models import *


def create_url(preference):
    """Return roommatepost create URL"""
    return reverse('students:postCreate', args=[preference])

def detail_url(post_id):
    """Return roommate post detail URL"""
    return reverse('students:postDetail', args=[post_id])

def update_delete_url(post_id):
    """Return roommate post delete URL"""
    return reverse('students:postDelete', args=[post_id])

def MockImage(ftype='.png'):
    with tempfile.NamedTemporaryFile(suffix=ftype, delete=False) as f:
        imageFile = Image.new('RGB', (200,200), 'white')
        imageFile.save(f, 'PNG')
    return open(f.name, mode='rb')

def sample_preference(name="cool"):
    """Return new sample preference object"""
    return Preference.objects.create(preferenceType=name)

def sample_interest(name="Sports"):
    return Interest.objects.create(interest=name)

def sample_roommate_post(student, preference="hours"):
    """Return new sample roommate post object"""
    pre = sample_preference(name=preference)
    int1 = sample_interest()
    int2 = sample_interest(name="Gym")
    int3 = sample_interest(name="coding")
    roompost = RoommatePost.objects.create(student=student, preference=pre, title="Sample Post",
                description="Body of the post", image="image1", image1="image2", image2="image3",
                image3="image4"
            )
    roompost.interest.set([int1, int2, int3])
    return roompost


class PublicRoommatePostApiTests(TestCase):
    """Test unauthenticated Roommate Post API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_create_roommate_post_required(self):
        """Test that authentication is required for creation of roommate post"""
        pre = sample_preference()
        res = self.client.get(create_url(pre.preferenceSlug))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_retrive_required_roommate_post(self):
        """Test that authentication is required for detail view roommate post"""
        res = self.client.get(detail_url(1))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_update_delete_required_roommate_post(self):
        """Test that authentication is required for update delete view roommate post"""
        res = self.client.get(update_delete_url(100))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateLandlordRoommatePostApiTests(TestCase):
    """Test Privately Roommate Post API no access using landlord user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testlandroommate', 
                    password="seller@123")
        usertype = UserType.objects.create(user=self.user, userType='seller')
        landlord =  UserLandLord.objects.create(user=usertype, phone="+12345678901", 
                    profilePicture="1.jpg",
                )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_no_access_create_roommate_post_required(self):
        """Test that landlord has no access for creation of roommate post"""
        res = self.client.get(create_url(20))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_access_retrive_roommate_post_required(self):
        """Test that landlord has no access for retrive of roommate post"""
        res = self.client.get(detail_url(2))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_no_access_update_delete_roommate_post_required(self):
        """Test that landlord has no access for update delete of roommate post"""
        res = self.client.get(update_delete_url(1))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateStudentRoommatePostApiTests(TestCase):
    """Test Privately available RoommatePost API access using Student user"""

    def setUp(self):
        self.student =  createStudent(username='studentlogin')
        self.user = get_user_model().objects.get(username='studentlogin')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.roommatepost = sample_roommate_post(student=self.student)

    def test_get_create_roommate_post(self):
        """Test that GET access for creation of roommatepost"""
        pre = sample_preference()
        res = self.client.get(create_url(pre.preferenceSlug))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_roommate_post(self):
        """Test that create roommate Post"""
        pre = sample_preference()
        int1 = sample_interest()
        int2 = sample_interest(name="Pool")
        payload = {
            "title": "Sample Piost",
            "description": "Description Post",
            "interest": [int1.pk, int2.pk],
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
            "image3": MockImage()
        }
        res = self.client.post(create_url(pre.preferenceSlug), payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        roompost = RoommatePost.objects.get(id=res.data['id'])

        serilizer = RoommatePostSerializer(roompost)
        
        self.assertEqual(payload['title'], roompost.title)
        self.assertEqual(payload['description'], roompost.description)
        interest = roompost.interest.all()
        self.assertIn(int1, interest)
        self.assertIn(int2, interest)
        self.assertTrue(os.path.exists(roompost.image.path))
        self.assertTrue(os.path.exists(roompost.image1.path))
        self.assertTrue(os.path.exists(roompost.image2.path))
        self.assertTrue(os.path.exists(roompost.image3.path))
        roompost.delete()
        self.assertFalse(os.path.exists(roompost.image.path))
        self.assertFalse(os.path.exists(roompost.image1.path))
        self.assertFalse(os.path.exists(roompost.image2.path))
        self.assertFalse(os.path.exists(roompost.image3.path))

    def test_create_invalid_preferences_roommatepost(self):
        """Test that create roommate post with invalid preferece slug"""
        int1 = sample_interest()
        payload = {
            "title": "Sample Piost",
            "description": "Description Post",
            "interest": [int1.pk],
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
        }
        res = self.client.post(create_url("asda-sadas"), payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_invalid1_fields_roommatepost(self):
        """Test that create invalid fields roommate post"""
        pre = sample_preference()
        int1 = sample_interest()
        int2 = sample_interest(name="Pool")
        payload = {
            "title": "",
            "description": "",
            "interest": [int1.pk, int2.pk, '10'],
            "image": MockImage(),
            "image1": MockImage(ftype='.mp4'),
            "image2": '',
        }
        res = self.client.post(create_url(pre.preferenceSlug), payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertEqual(res.data.get('title')[0], exceptions.ErrorDetail("This field may not be blank.", code="blank"))
        self.assertEqual(res.data.get('description')[0], exceptions.ErrorDetail("This field may not be blank.", code="blank"))
        self.assertEqual(res.data.get('interest')[0], exceptions.ErrorDetail('Invalid pk "10" - object does not exist.', code="does_not_exist"))

    def test_retrive_roommatepost_detail(self):
        """Test that retrive roommate post"""
        std = createStudent(username='otherstdient')
        roommatePost = sample_roommate_post(student=std)

        res = self.client.get(detail_url(self.roommatepost.pk))
        serilizer = RoommatePostDetailSerializer(self.roommatepost)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in res.data.keys():
            if 'image' in key:
                self.assertEqual(res.data[key], 'http://testserver{}'.format(serilizer.data[key]))
            else:
                self.assertEqual(res.data[key], serilizer.data[key])

        #other user post
        res = self.client.get(detail_url(roommatePost.pk))
        serilizer = RoommatePostDetailSerializer(roommatePost)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in res.data.keys():
            if 'image' in key:
                self.assertEqual(res.data[key], 'http://testserver{}'.format(serilizer.data[key]))
            else:
                self.assertEqual(res.data[key], serilizer.data[key])
    
    def test_update_roommates_partial_post(self):
        """Test that update partial roommates post"""
        payload = {
            "title": "Sample Piost sdsdf",
            "description": "Description sdfsd Post",
        }
        res = self.client.patch(update_delete_url(self.roommatepost.id), payload, format='multipart')
        
        self.roommatepost.refresh_from_db()
        
        serilizer = RoommatePostSerializer(self.roommatepost)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.roommatepost, key))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in res.data.keys():
            if 'image' in key:
                self.assertEqual(res.data[key], 'http://testserver{}'.format(serilizer.data[key]))
            else:
                self.assertEqual(res.data[key], serilizer.data[key])


    def test_update_roommates_full_post(self):
        """Test that update full roommates post"""
        int1 = sample_interest(name="new")
        payload = {
            "title": "Sample Piost sdfds",
            "description": "Description Post sdfds",
            "interest": [int1.pk],
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
            "image3": MockImage()
        }
        res = self.client.put(update_delete_url(self.roommatepost.id), payload, format='multipart')
        
        self.roommatepost.refresh_from_db()
        
        serilizer = RoommatePostSerializer(self.roommatepost)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in res.data.keys():
            if 'image' in key:
                self.assertEqual(res.data[key], 'http://testserver{}'.format(serilizer.data[key]))
            else:
                self.assertEqual(res.data[key], serilizer.data[key])

        self.assertTrue(os.path.exists(self.roommatepost.image.path))
        self.assertTrue(os.path.exists(self.roommatepost.image1.path))
        self.assertTrue(os.path.exists(self.roommatepost.image2.path))
        self.assertTrue(os.path.exists(self.roommatepost.image3.path))
        payload = {
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
            "image3": MockImage()
        }
        res = self.client.patch(update_delete_url(self.roommatepost.id), payload, format='multipart')
        self.assertFalse(os.path.exists(self.roommatepost.image.path))
        self.assertFalse(os.path.exists(self.roommatepost.image1.path))
        self.assertFalse(os.path.exists(self.roommatepost.image2.path))
        self.assertFalse(os.path.exists(self.roommatepost.image3.path))

        self.roommatepost.refresh_from_db()
        self.roommatepost.delete()

    def test_update_invalid_roommatepost(self):
        """Test that update invalid RoommatePost which is not there"""
        payload = {
            "title": "Sample Piost sdfds",
            "description": "Description Post sdfds",
            "interest": ['10'],
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
            "image3": MockImage()
        }
        res = self.client.put(update_delete_url(100), payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_invalid_field_roommates_post(self):
        """Test that update with invalid fields Roommates Post """
        payload = {
            "title": "",
            "description": "",
            "interest": '',
            "image": '',
            "image1": '',
            "image2": '',
            "image3": MockImage('.mp4')
        }
        res = self.client.put(update_delete_url(self.roommatepost.id), payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.roommatepost.refresh_from_db()

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(self.roommatepost, key))

    def test_update_other_user_roommates_post(self):
        """Test that update other user Roommate Post"""
        int1 = sample_interest(name="new")
        std = createStudent(username='otherstudentowner')
        roompost = sample_roommate_post(student=std)
        payload = {
            "title": "Sample Piost sdfds",
            "description": "Description Post sdfds",
            "interest": [int1.pk],
            "image": MockImage(),
            "image1": MockImage(),
            "image2": MockImage(),
            "image3": MockImage()
        }
        res = self.client.put(update_delete_url(roompost.id), payload, format='multipart')
        
        roompost.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(roompost, key))

    def test_delete_roommate_post(self):
        """Test that delete roommate post"""
        res = self.client.delete(update_delete_url(self.roommatepost.pk))
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RoommatePost.objects.filter(pk=self.roommatepost.pk).exists())
    
    def test_delete_other_user_roommate_post(self):
        """Test that delete other user Roommate Post"""
        std = createStudent(username='otherstdient')
        roommatePost = sample_roommate_post(student=std)
        res = self.client.delete(update_delete_url(roommatePost.id))
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(RoommatePost.objects.filter(pk=roommatePost.pk).exists())