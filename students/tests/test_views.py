from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

from property.tests.test_models import sampleProperty
from students.tests.test_roommates_api import sample_roommate_post, sample_preference
from students.tests.test_models import createStudent
from users.models import UserLandLord, UserType
from students.models import *

client = Client()

def samplefavourite(student):
    """creates sample favouirtes and returns the object property"""
    prop = sampleProperty()
    if Favourite.objects.filter(student=student).exists():
        fav = Favourite.objects.get(student=student)
        fav.properties.add(prop)
    else:
        fav = Favourite.objects.create(student=student)
        fav.properties.add(prop)
    fav.save()
    return prop

class PrivateAccessTests(TestCase):
    """Test View request that require authentication of login"""

    def test_favourite_list_view(self):
        """Test get & post request login required for favourite list view"""

        response = client.get(reverse('students:favourites'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/')

        response = client.post(reverse('students:favourites'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/')

    def test_favourite_add_view(self):
        """Test get & post request login required for favourite add view"""
        prop = sampleProperty()
        response = client.get(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/add/{}/'.format(prop.urlSlug))

        response = client.post(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/add/{}/'.format(prop.urlSlug))

    def test_favourite_remove_view(self):
        """Test get & post request login required for favourite remove view"""
        prop = sampleProperty()
        response = client.get(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/remove/{}/'.format(prop.urlSlug))

        response = client.post(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/favourites/remove/{}/'.format(prop.urlSlug))
    
    def test_heart_add_remove_view(self):
        """Test get & post request login required for heart add and remove view"""
        std = createStudent(username='studentheart')
        post = sample_roommate_post(student=std)
        response = client.get(reverse('students:addRemoveHeart', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/post/{}/heart/'.format(post.pk))

        response = client.post(reverse('students:addRemoveHeart', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/post/{}/heart/'.format(post.pk))
    
    def test_roommates_post_list_allpost_view(self):
        """Test get & post request login required for roommates post list view All post"""
        response = client.get(reverse('students:roommates'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/')

        response = client.post(reverse('students:roommates'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/')
    
    def test_roommates_post_list_mypost_view(self):
        """Test get & post request login required for roommates post list view mypost"""
        response = client.get(reverse('students:roommatesMypost'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/mypost/')

        response = client.post(reverse('students:roommatesMypost'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/roommates/mypost/')

    # def test_roommates_post_list_preferences_view(self):
    #     """Test get & post request login required for roommates post list view preferences"""
    #     pre = sample_preference()
    #     response = client.get(reverse('students:roommatesPreference', kwargs={'preference': pre.preferenceSlug}))
    #     self.assertEqual(response.status_code, HTTPStatus.FOUND)
    #     self.assertEqual(response.url, '/?next=/roommates/{}/'.format(pre.preferenceSlug))

    #     response = client.post(reverse('students:roommatesPreference', kwargs={'preference': pre.preferenceSlug}))
    #     self.assertEqual(response.status_code, HTTPStatus.FOUND)
    #     self.assertEqual(response.url, '/?next=/roommates/{}/'.format(pre.preferenceSlug))


class PrivateLandlordAccessStudentAppTests(TestCase):
    """
    Test student App View request that landlord should not be accessed.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testlandroommateview', 
                    password="seller@123")
        usertype = UserType.objects.create(user=self.user, userType='seller')
        landlord =  UserLandLord.objects.create(user=usertype, phone="+12345678901", 
                    profilePicture="1.jpg",
                )
        self.client = client
        self.client.force_login(user=self.user)

    def test_favourite_list_view_as_landlord(self):
        """Test get & post request for favourite list view as landlord"""

        response = client.get(reverse('students:favourites'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = client.post(reverse('students:favourites'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    
    def test_favourite_add_view_as_landlord(self):
        """Test get & post request for favourite add view as landlord"""
        prop = sampleProperty()
        response = client.get(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_favourite_remove_view_as_landlord(self):
        """Test get & post request for favourite remove view as landlord"""
        prop = sampleProperty()
        response = client.get(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    def test_heart_add_remove_view_as_landlord(self):
        """Test get & post request for heart add and remove view as landlord"""
        std = createStudent(username='studentheart')
        post = sample_roommate_post(student=std)
        response = client.get(reverse('students:addRemoveHeart', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:addRemoveHeart', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    def test_roommates_post_list_allpost_view_as_landlord(self):
        """Test get & post request for roommates post list view allpost as landlord"""
        response = client.get(reverse('students:roommates'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = client.post(reverse('students:roommates'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_roommates_post_list_mypost_view_as_landlord(self):
        """Test get & post request for roommates post list view mypost as landlord"""
        response = client.get(reverse('students:roommatesMypost'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = client.post(reverse('students:roommatesMypost'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    
    # def test_roommates_post_list_preferences_view_as_landlord(self):
    #     """Test get & post request login roommates post list view preferences as landlord"""
    #     pre = sample_preference()
    #     response = client.get(reverse('students:roommatesPreference', kwargs={'preference': pre.preferenceSlug}))
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    #     response = client.post(reverse('students:roommatesPreference', kwargs={'preference': pre.preferenceSlug}))
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class PrivateStudentAccessStudentAppTests(TestCase):
    """
    Test Student App View request that require authentication of Student and only student can
    access that.
    """

    def setUp(self):
        self.student =  createStudent(username='studentloginroommate')
        self.user = get_user_model().objects.get(username='studentloginroommate')
        self.client = client
        self.client.force_login(user=self.user)

    def test_favourite_list_view_returns_for_current_user(self):
        """ Test get method of favourite list view that object returned is of current user"""
        std2 = createStudent(username='otherfavouite')
        fav1 = samplefavourite(self.student)
        fav2 = samplefavourite(self.student)
        fav3 = samplefavourite(self.student)
        fav4 = samplefavourite(std2)

        favObj = Favourite.objects.get(student=self.student)

        response = client.get(reverse('students:favourites'))
        resdata = list(response.context.get('object_list'))
        realdata = list(resdata[0].properties.all())
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(favObj.properties.count(), 3)
        self.assertIn(fav1, realdata)
        self.assertIn(fav2, realdata)
        self.assertIn(fav3, realdata)
        self.assertNotIn(fav4, realdata)

        response = client.post(reverse('students:favourites'))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_favourite_add_view_get(self):
        """Test the get request of add favourites view as student user"""
        prop = sampleProperty()
        response = client.get(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop.urlSlug))

    def test_favourite_add_view_as_new_user(self):
        """Test the post request of add favourites view as student new user"""
        prop = sampleProperty()
        self.assertFalse(Favourite.objects.filter(student=self.student).exists())
        response = client.post(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Favourite.objects.filter(student=self.student).exists())
        fav = Favourite.objects.get(student=self.student)
        self.assertTrue(response.json().get('added'))
        self.assertIn(prop, fav.properties.all())

    def test_favourite_add_view_as_old_user(self):
        """Test the post request of add favourites view as student old user"""
        fav1 = samplefavourite(self.student)
        prop = sampleProperty()
        self.assertTrue(Favourite.objects.filter(student=self.student).exists())
        response = client.post(reverse('students:addFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        fav = Favourite.objects.get(student=self.student)
        self.assertTrue(response.json().get('added'))
        self.assertEqual(fav.properties.count(), 2)
        self.assertIn(prop, fav.properties.all())
        self.assertIn(fav1, fav.properties.all())
    
    def test_favourite_add_view_as_invalid_property(self):
        """Test the get & post request of add favourites with invalid property"""

        response = client.get(reverse('students:addFavourites', kwargs={'slug': 'sadas-asda'}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:addFavourites', kwargs={'slug': 'asdada-asdas'}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    def test_favourite_add_view_already_added_property(self):
        """Test the post request of add favourites where the property already added as favourite"""
        fav1 = samplefavourite(self.student)
        self.assertTrue(Favourite.objects.filter(student=self.student).exists())
        response = client.post(reverse('students:addFavourites', kwargs={'slug': fav1.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        fav = Favourite.objects.get(student=self.student)
        self.assertFalse(response.json().get('added'))
        self.assertEqual(fav.properties.count(), 1)
        self.assertIn(fav1, fav.properties.all())

    def test_favourite_remove_view_get(self):
        """Test the get request of remove favourites view as student user"""
        prop = sampleProperty()
        response = client.get(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop.urlSlug))
    
    def test_favourite_remove_view_as_new_user(self):
        """Test the post request of remove favourites view as student new user"""
        prop = sampleProperty()
        self.assertFalse(Favourite.objects.filter(student=self.student).exists())
        response = client.post(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertFalse(Favourite.objects.filter(student=self.student).exists())

    def test_favourite_remove_view_as_old_user_valid_property(self):
        """Test the post request of remove favourites view as student old user with valid property"""
        fav1 = samplefavourite(self.student)
        self.assertTrue(Favourite.objects.filter(student=self.student).exists())
        fav = Favourite.objects.get(student=self.student)
        self.assertIn(fav1, fav.properties.all())
        response = client.post(reverse('students:removeFavourites', kwargs={'slug': fav1.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json().get('removed'))
        fav.refresh_from_db()
        self.assertEqual(fav.properties.count(), 0)
        self.assertNotIn(fav1, fav.properties.all())
    
    def test_favourite_remove_view_as_invalid_property(self):
        """Test the get & post request of remove favourites with invalid property"""

        response = client.get(reverse('students:removeFavourites', kwargs={'slug': 'sadas-asda'}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:removeFavourites', kwargs={'slug': 'asdada-asdas'}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_favourite_remove_view_property_not_marked(self):
        """Test the post request of remove favourites where the property not added as favourite"""
        fav1 = samplefavourite(self.student)
        prop = sampleProperty()
        self.assertTrue(Favourite.objects.filter(student=self.student).exists())
        response = client.post(reverse('students:removeFavourites', kwargs={'slug': prop.urlSlug}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        fav = Favourite.objects.get(student=self.student)
        self.assertFalse(response.json().get('removed'))
        self.assertEqual(fav.properties.count(), 1)
        self.assertIn(fav1, fav.properties.all())
        self.assertNotIn(prop, fav.properties.all())

    def test_heart_add_remove_view_get(self):
        """Test the get request of add remove hearts view as student user"""
        std = createStudent(username='roomotheruser')
        roompost = sample_roommate_post(student=std)
        response = client.get(reverse('students:addRemoveHeart', kwargs={'pk': roompost.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/roommates/')

    def test_heart_add_view_for_post(self):
        """Test the post request of adding heart as student user"""
        std = createStudent(username='roomotheruser')
        roompost = sample_roommate_post(student=std)
        roompost.heart.add(std)
        self.assertEqual(roompost.totalHearts(), 1)
        self.assertIn(std, roompost.heart.all())
        response = client.post(reverse('students:addRemoveHeart', kwargs={'pk': roompost.pk}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json().get('hearted'))
        roompost.refresh_from_db()
        self.assertEqual(response.json().get('total'), roompost.totalHearts())
        self.assertEqual(response.json().get('total'), roompost.heart.count())
        self.assertIn(self.student, roompost.heart.all())

    def test_heart_remove_view_for_post(self):
        """Test the post request of removing heart as student user"""
        std = createStudent(username='roomotheruser')
        roompost = sample_roommate_post(student=std)
        roompost.heart.add(std)
        roompost.heart.add(self.student)
        self.assertEqual(2, roompost.totalHearts())
        self.assertEqual(2, roompost.heart.count())
        response = client.post(reverse('students:addRemoveHeart', kwargs={'pk': roompost.pk}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.json().get('hearted'))
        roompost.refresh_from_db()
        self.assertEqual(response.json().get('total'), roompost.totalHearts())
        self.assertEqual(response.json().get('total'), roompost.heart.count())
        self.assertNotIn(self.student, roompost.heart.all())
        self.assertIn(std, roompost.heart.all())
    
    def test_heart_add_remove_view_as_invalid_post(self):
        """Test the get & post request of add remove heart with invalid post"""

        response = client.get(reverse('students:addRemoveHeart', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('students:addRemoveHeart', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_roommate_all_post_check_get(self):
        """ Test that /roommates/ url return all post"""
        po1 = sample_roommate_post(student=self.student)
        po2 = sample_roommate_post(student=self.student)
        po3 = sample_roommate_post(student=self.student)
        po4 = sample_roommate_post(student=self.student)
        std = createStudent(username='roomotheruser')
        op1 = sample_roommate_post(student=std)
        op2 = sample_roommate_post(student=std)

        response = client.get(reverse('students:roommates'))
        objectlist = list(response.context.get('object_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(objectlist), 6)
        self.assertEqual(op2, objectlist[0])
        self.assertEqual(op1, objectlist[1])
        self.assertEqual(po4, objectlist[2])
        self.assertEqual(po3, objectlist[3])
        self.assertEqual(po2, objectlist[4])
        self.assertEqual(po1, objectlist[5])
        # self.assertEqual(response.context.get('currentpreferences', None), None)
    
    def test_roommate_my_post_check_get(self):
        """ Test that /roommates/mypost/ url return only the post the current user posted """
        po1 = sample_roommate_post(student=self.student)
        po2 = sample_roommate_post(student=self.student)
        po3 = sample_roommate_post(student=self.student)
        po4 = sample_roommate_post(student=self.student)
        std = createStudent(username='roomotheruser')
        op1 = sample_roommate_post(student=std)
        op2 = sample_roommate_post(student=std)

        response = client.get(reverse('students:roommatesMypost'))
        objectlist = list(response.context.get('object_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(objectlist), 4)
        self.assertEqual(po4, objectlist[0])
        self.assertEqual(po3, objectlist[1])
        self.assertEqual(po2, objectlist[2])
        self.assertEqual(po1, objectlist[3])
        # self.assertEqual(response.context.get('currentpreferences', None), None)

    # def test_roommate_preference_post_check_get(self):
    #     """ Test that only the post with that preference is returened"""
    #     po1 = sample_roommate_post(student=self.student)
    #     po2 = sample_roommate_post(student=self.student)
    #     po3 = sample_roommate_post(student=self.student, preference='hours sports')
    #     po4 = sample_roommate_post(student=self.student, preference='hours sports')
    #     std = createStudent(username='roomotheruser')
    #     op1 = sample_roommate_post(student=std)
    #     op2 = sample_roommate_post(student=std, preference='hours sports')

    #     response = client.get(reverse('students:roommatesPreference', kwargs={'preference': po1.preference.preferenceSlug}))
    #     objectlist = list(response.context.get('object_list'))
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertEqual(len(objectlist), 3)
    #     self.assertEqual(op1, objectlist[0])
    #     self.assertEqual(po2, objectlist[1])
    #     self.assertEqual(po1, objectlist[2])
    #     self.assertEqual(response.context.get('currentpreferences'), po1.preference)

    #     response = client.get(reverse('students:roommatesPreference', kwargs={'preference': po3.preference.preferenceSlug}))
    #     objectlist = list(response.context.get('object_list'))
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertEqual(len(objectlist), 3)
    #     self.assertEqual(op2, objectlist[0])
    #     self.assertEqual(po4, objectlist[1])
    #     self.assertEqual(po3, objectlist[2])
    #     self.assertEqual(response.context.get('currentpreferences'), po3.preference)
    
    def test_roommates_post_list_view_post_request(self):
        """Test post request for roommates post list view"""
        response = client.post(reverse('students:roommates'))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        # pre = sample_preference()
        
        # response = client.post(reverse('students:roommatesPreference', kwargs={'preference': pre.preferenceSlug}))
        # self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        response = client.post(reverse('students:roommatesMypost'))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        

    # def test_roommates_post_list_view_invalid_preferences(self):
    #     """Test get and post request for roommates post list view with invalid prefereces"""

    #     response = client.get(reverse('students:roommatesPreference', kwargs={'preference': 'asdas-sad'}))
    #     self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
    #     response = client.post(reverse('students:roommatesPreference', kwargs={'preference': 'asdas-asd'}))
    #     self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)