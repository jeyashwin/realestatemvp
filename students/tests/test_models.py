from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
import os

from property.tests.test_views import sampleProperty, MockImageVideo
from students.models import *
from users.models import *

def createStudent(username="studentroommates"):
    user = get_user_model().objects.create_user(username=username, password="Student@123")
    usertype = UserType.objects.create(user=user, userType='student')
    student = UserStudent.objects.create(user=usertype, phone="+12345678901", 
                    university='Test college', classYear=2015, bio="test bio data", 
                    profilePicture="1.jpg",
                )
    return student

def createRoommatesPost(student=None):
    # int1 = Interest.objects.create(interest="sports")
    # int2 = Interest.objects.create(interest="gym")
    # int3 = Interest.objects.create(interest="coding")
    img = MockImageVideo(ftype='jpg')
    img1 = MockImageVideo(ftype='jpg')
    img2 = MockImageVideo(ftype='jpg')
    img3 = MockImageVideo()
    if student is None:
        student = createStudent()
    # prefObj = Preference.objects.create(preferenceType="Quiet hours")
    #  preference=prefObj,
    roomObj = RoommatePost.objects.create(student=student,
                    title="New post", description="Welcome to new post", image=img.name, 
                    image1=img1.name, image2=img2.name, 
                    image3=img3.name
                )
    # roomObj.interest.set([int1, int2, int3])
    roomObj.heart.set([createStudent(username="123"), createStudent(username="1234")])
    return roomObj

class StudentModelTests(TestCase):
    """ Test all the  models in Student App"""

    def test_favourite_model_str(self):
        """Test the favourite model string representation"""
        studentObj = createStudent()
        propobject = sampleProperty()
        propobject1 = sampleProperty()
        favouriteObj = Favourite.objects.create(student=studentObj)
        favouriteObj.properties.set([propobject, propobject1])

        self.assertEqual(str(favouriteObj), str(favouriteObj.pk))
        self.assertEqual(list(favouriteObj.properties.all()), [propobject, propobject1])

    # def test_preference_model_str(self):
    #     """Test the preference model string representation"""
    #     pref = Preference.objects.create(preferenceType="Quiet hours")
    #     pref1 = Preference.objects.create(preferenceType="Sleep")
    #     pref2 = Preference.objects.create(preferenceType="Sleep")

    #     self.assertEqual(str(pref), pref.preferenceType)
    #     self.assertEqual(pref.preferenceSlug, "quiet-hours")
    #     self.assertEqual(str(pref1), pref1.preferenceType)
    #     self.assertEqual(pref1.preferenceSlug, "sleep")
    #     self.assertEqual(str(pref2), pref2.preferenceType)
    #     self.assertIn("sleep", pref2.preferenceSlug)

    def test_roommatepost_model_str(self):
        """Test the RoommatePost model string representation"""
        post = createRoommatesPost()

        self.assertEqual(post.totalHearts(), 2)
        self.assertEqual(str(post), post.title)
        # self.assertEqual(post.preference.preferenceType, "Quiet hours")
        self.assertEqual(post.student.user.user.username, "studentroommates")
        heart = post.heart.first()
        self.assertEqual(heart.user.user.username, "123")
    
    def test_postcomment_model_str(self):
        """Test the PostComment model string representation"""
        comment = PostComment.objects.create(roomatePost=createRoommatesPost(), 
                        student=createStudent(username='comment'), comment="That's cool"
                    )
        self.assertEqual(str(comment), comment.comment)

    def test_commentreply_model_str(self):
        """Test the CommentReply model string representation"""
        comment = PostComment.objects.create(roomatePost=createRoommatesPost(), 
                        student=createStudent(username='comment'), comment="That's cool"
                    )
        reply = CommentReply.objects.create(comment=comment, student=createStudent(username='reply'), 
                    reply="Wow amazing"
                )
        self.assertEqual(str(reply), reply.reply)
        self.assertEqual(reply.comment, comment)
        self.assertEqual(reply.student.user.user.username, "reply")

    @patch('uuid.uuid4')
    def test_post_image_file_name_uuid(self, mock_uuid):
        """Test that roommates post image is saved in a correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = roompost_image_file_path(None, 'sampleimage.jpg')
        exp_path = f'uploads/post/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)