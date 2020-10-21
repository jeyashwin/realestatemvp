from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.serializers import PostCommentSerializer
from students.models import PostComment, CommentReply
from students.tests.test_models import createStudent, createRoommatesPost
from users.models import *


def create_url(post_id):
    """Return comment create URL"""
    return reverse('students:commentCreate', args=[post_id])

def retrive_update_delete(comment_id):
    """Return comment retrive update delete URL"""
    return reverse('students:commentUpdateDelete', args=[comment_id])

def sample_comment(student):
    """Return new sample comment object"""
    post = createRoommatesPost()
    return PostComment.objects.create(roomatePost=post, student=student, comment="test comment")

def sample_reply(student, comment):
    """Return new sample reply object"""
    return CommentReply.objects.create(comment=comment, student=student, reply="test reply")


class PublicCommentApiTests(TestCase):
    """Test unauthenticated Comment API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_create_required(self):
        """Test that authentication is required for creation"""
        res = self.client.get(create_url(1))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_retrive_update_delete_required(self):
        """Test that authentication is required for retrive"""
        res = self.client.get(retrive_update_delete(1))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateLandlordCommentApiTests(TestCase):
    """Test Privately Comment API no access using landlord user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testlandcomment', 
                    password="seller@123")
        usertype = UserType.objects.create(user=self.user, userType='seller')
        landlord =  UserLandLord.objects.create(user=usertype, phone="+12345678901", 
                    profilePicture="1.jpg",
                )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_no_access_create_required(self):
        """Test that landlord has no access for creation"""
        res = self.client.get(create_url(2))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_access_retrive_update_delete_required(self):
        """Test that landlord has no access for retrive"""
        res = self.client.get(retrive_update_delete(2))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateStudentCommentApiTests(TestCase):
    """Test Privately available Comment API access using Student user"""

    def setUp(self):
        self.student =  createStudent(username='studentlogin')
        self.user = get_user_model().objects.get(username='studentlogin')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_comment(self):
        """Test that GET access for creation"""
        post = createRoommatesPost()
        res = self.client.get(create_url(post.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_comment(self):
        """Test that create Comment"""
        post = createRoommatesPost()
        payload = {
            'comment': "Hello Everyone"
        }
        res = self.client.post(create_url(post.id), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = PostComment.objects.get(id=res.data['id'])

        serilizer = PostCommentSerializer(comment)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(comment, key))

        self.assertEqual(res.data, serilizer.data)
    
    def test_create_invalid_post_comment(self):
        """Test that create comment with invalid post Comment"""
        payload = {
            'comment': "Hello Everyone bye"
        }
        res = self.client.post(create_url(100), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_invalid_field_comment(self):
        """Test that create invalid field Comment"""
        post = createRoommatesPost()
        payload = {
            'comment': ""
        }
        res = self.client.post(create_url(post.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_comment(self):
        """Test that retrive Comment"""
        comment = sample_comment(student=self.student)
        res = self.client.get(retrive_update_delete(comment.id))

        serilizer = PostCommentSerializer(comment)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_retrive_comment_different_user(self):
        """Test that retrive Comment of other user"""
        std = createStudent(username='otherowner')
        comment = sample_comment(student=std)
        res = self.client.get(retrive_update_delete(comment.id))

        serilizer = PostCommentSerializer(comment)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment(self):
        """Test that update Comment"""
        comment = sample_comment(student=self.student)
        rep1 = sample_reply(student=createStudent(username='reply'), comment=comment)
        rep2 = sample_reply(student=createStudent(username='reply1'), comment=comment)
        payload = {
            'comment': "hello"
        }
        res = self.client.put(retrive_update_delete(comment.id), payload)
        
        comment.refresh_from_db()
        
        serilizer = PostCommentSerializer(comment)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(comment, key))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_update_invalid_comment(self):
        """Test that update invalid Comment which is not there"""
        payload = {
            'comment': "hello"
        }
        res = self.client.put(retrive_update_delete(100), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_invalid_field_comment(self):
        """Test that update with invalid fields Comment """
        comment = sample_comment(student=self.student)
        payload = {
            'comment': ""
        }
        res = self.client.put(retrive_update_delete(comment.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        comment.refresh_from_db()

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(comment, key))

    def test_update_other_user_comment(self):
        """Test that update other user Comment"""
        std = createStudent(username='otherowner')
        comment = sample_comment(student=std)
        payload = {
            'comment': "hello"
        }
        res = self.client.put(retrive_update_delete(comment.id), payload)
        
        comment.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(comment, key))
    
    def test_delete_comment(self):
        """Test that delete Comment"""
        comment = sample_comment(student=self.student)
        res = self.client.delete(retrive_update_delete(comment.id))
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostComment.objects.filter(pk=comment.pk).exists())
    
    def test_delete_other_user_comment(self):
        """Test that delete other user Comment"""
        std = createStudent(username='otherowner')
        comment = sample_comment(student=std)
        res = self.client.delete(retrive_update_delete(comment.id))
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(PostComment.objects.filter(pk=comment.pk).exists())