from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.serializers import CommentReplySerializer
from students.models import PostComment, CommentReply
from students.tests.test_models import createStudent, createRoommatesPost
from users.models import *


def create_url(comment_id):
    """Return reply create URL"""
    return reverse('students:replyCreate', args=[comment_id])

def retrive_update_delete(reply_id):
    """Return reply retrive update delete URL"""
    return reverse('students:replyUpdateDelete', args=[reply_id])

def sample_comment():
    """Return new sample comment object"""
    post = createRoommatesPost()
    student = createStudent(username='samplecomment')
    return PostComment.objects.create(roomatePost=post, student=student, comment="test comment")

def sample_reply(student):
    """Return new sample reply object"""
    comment = sample_comment()
    return CommentReply.objects.create(comment=comment, student=student, reply="test reply")


class PublicReplyApiTests(TestCase):
    """Test unauthenticated Reply API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_create_reply_required(self):
        """Test that authentication is required for creation of reply"""
        res = self.client.get(create_url(100))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_retrive_update_delete_required_reply(self):
        """Test that authentication is required for retrive reply"""
        res = self.client.get(retrive_update_delete(202))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateLandlordReplyApiTests(TestCase):
    """Test Privately Reply API no access using landlord user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testlandreply', 
                    password="seller@123")
        usertype = UserType.objects.create(user=self.user, userType='seller')
        landlord =  UserLandLord.objects.create(user=usertype, phone="+12345678901", 
                    profilePicture="1.jpg",
                )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_no_access_create_reply_required(self):
        """Test that landlord has no access for creation of reply"""
        res = self.client.get(create_url(20))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_access_retrive_update_delete_reply_required(self):
        """Test that landlord has no access for retrive of reply"""
        res = self.client.get(retrive_update_delete(2))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateStudentReplyApiTests(TestCase):
    """Test Privately available Reply API access using Student user"""

    def setUp(self):
        self.student =  createStudent(username='studentlogin')
        self.user = get_user_model().objects.get(username='studentlogin')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_reply(self):
        """Test that GET access for creation of reply"""
        comment = sample_comment()
        res = self.client.get(create_url(comment.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_reply(self):
        """Test that create reply"""
        comment = sample_comment()
        payload = {
            'reply': "This is correct"
        }
        res = self.client.post(create_url(comment.id), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reply = CommentReply.objects.get(id=res.data['id'])

        serilizer = CommentReplySerializer(reply)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(reply, key))

        self.assertEqual(res.data, serilizer.data)

    def test_create_invalid_comment_reply(self):
        """Test that create reply with invalid comment id"""
        payload = {
            'reply': "bye"
        }
        res = self.client.post(create_url(100), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_invalid_field_reply(self):
        """Test that create invalid field Reply"""
        comment = sample_comment()
        payload = {
            'reply': ""
        }
        res = self.client.post(create_url(comment.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_reply(self):
        """Test that retrive Reply"""
        reply = sample_reply(student=self.student)
        res = self.client.get(retrive_update_delete(reply.id))

        serilizer = CommentReplySerializer(reply)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_retrive_reply_different_user(self):
        """Test that retrive Reply of other user"""
        std = createStudent(username='otherowner')
        reply = sample_reply(student=std)
        res = self.client.get(retrive_update_delete(reply.id))

        serilizer = CommentReplySerializer(reply)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reply(self):
        """Test that update Reply"""
        reply = sample_reply(student=self.student)
        payload = {
            'reply': "hello"
        }
        res = self.client.put(retrive_update_delete(reply.id), payload)
        
        reply.refresh_from_db()
        
        serilizer = CommentReplySerializer(reply)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(reply, key))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_update_invalid_reply(self):
        """Test that update invalid Reply which is not there"""
        payload = {
            'reply': "hello bte"
        }
        res = self.client.put(retrive_update_delete(100), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_invalid_field_reply(self):
        """Test that update with invalid fields Reply """
        reply = sample_reply(student=self.student)
        payload = {
            'reply': ""
        }
        res = self.client.put(retrive_update_delete(reply.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        reply.refresh_from_db()

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(reply, key))

    def test_update_other_user_reply(self):
        """Test that update other user Reply"""
        std = createStudent(username='otherowner')
        reply = sample_reply(student=std)
        payload = {
            'reply': "hello"
        }
        res = self.client.put(retrive_update_delete(reply.id), payload)
        
        reply.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        for key in payload.keys():
            self.assertNotEqual(payload[key], getattr(reply, key))
    
    def test_delete_reply(self):
        """Test that delete Reply"""
        reply = sample_reply(student=self.student)
        res = self.client.delete(retrive_update_delete(reply.id))
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CommentReply.objects.filter(pk=reply.pk).exists())
    
    def test_delete_other_user_reply(self):
        """Test that delete other user Reply"""
        std = createStudent(username='otherowner')
        reply = sample_reply(student=std)
        res = self.client.delete(retrive_update_delete(reply.id))
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CommentReply.objects.filter(pk=reply.pk).exists())