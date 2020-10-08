from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from PIL import Image
import datetime, tempfile, os

from property.tests.test_models import sampleProperty
from property import models as propmodel
from users.tests.test_views import createLandlordUser, createStudentUser
from users import models

client = Client()

def MockImageVideo(ftype='.png'):
    with tempfile.NamedTemporaryFile(suffix=ftype, delete=False) as f:
        imageFile = Image.new('RGB', (200,200), 'white')
        imageFile.save(f, 'PNG')
    return open(f.name, mode='rb')

def amenity(name="Wifi"):
    return propmodel.Amenities.objects.create(amenityType=amenity)

def city():
    state = propmodel.StateList.objects.create(stateFullName="Ozark", stateShortName="OZ")
    return propmodel.CityList.objects.create(state=state, cityName="Los Angeles")

class PrivateAccessTests(TestCase):
    """Test View request that require authentication of login"""

    def test_property_create_view(self):
        """Test get & post request login required for property create view"""

        response = client.get(reverse('property:propertyCreate'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/create/')

        response = client.post(reverse('property:propertyCreate'), data={'title': "new property"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/create/')
    
    def test_property_update_view(self):
        """Test get & post request login required for property update view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/update/{}/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}), 
                    data={'title': "new property"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/update/{}/'.format(prop.urlSlug))

    def test_property_delete_view(self):
        """Test get & post request login required for property delete view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/delete/{}/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/delete/{}/'.format(prop.urlSlug))

    def test_landlord_manage_property_view(self):
        """Test get & post request login required for landlord manage property view"""
        response = client.get(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/myproperty/')

        response = client.post(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/myproperty/')

    def test_property_list_view(self):
        """Test get & post request login required for property list view"""
        response = client.get(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/')

        response = client.post(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/')

    def test_property_detail_view(self):
        """Test get & post request login required for property detail view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyDetail', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/{}/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyDetail', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/{}/'.format(prop.urlSlug))

    def test_property_likes_dislikes_view(self):
        """Test get & post request login required for property likes and dislikes view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/reaction/{}/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/reaction/{}/'.format(prop.urlSlug))

    def test_post_question_view(self):
        """Test get & post request login required for post question view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyQuestion', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/question/{}/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyQuestion', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/question/{}/'.format(prop.urlSlug))

    def test_post_answer_view(self):
        """Test get & post request login required for post answer view"""
        prop = sampleProperty()
        response = client.get(reverse('property:propertyAnswer', kwargs={'slug': prop.urlSlug, 'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/answer/{}/1/'.format(prop.urlSlug))

        response = client.post(reverse('property:propertyAnswer', kwargs={'slug': prop.urlSlug, 'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/property/answer/{}/1/'.format(prop.urlSlug))


class PrivateLandlordAccessTests(TestCase):
    """
    Test View request that require authentication of landlord and view request that should
    not be accessed by landlord.
    """

    def setUp(self):
        self.landlord = createLandlordUser()
        self.client = client
        self.client.force_login(user=self.landlord)

    def test_property_create_landlord_access(self):
        """Test get & post request for property create view as logged in landlord user"""

        response = self.client.get(reverse('property:propertyCreate'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('user'), self.landlord)

        response = self.client.post(reverse('property:propertyCreate'), 
                    data={'title': "new property", 'fromDate': datetime.date.today(), 
                            'toDate':datetime.date.today(), 'propertyimage_set-TOTAL_FORMS': 4,
                            'propertyimage_set-INITIAL_FORMS': 4, 'propertyimage_set-MAX_NUM_FORMS': 10,
                            'propertyvideo_set-TOTAL_FORMS': 1, 'propertyvideo_set-INITIAL_FORMS': 1, 
                            'propertyvideo_set-MAX_NUM_FORMS': 4
                        }
                )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(propmodel.Property.objects.filter(urlSlug="new-property").exists())

    def test_property_update_landlord_access(self):
        """Test get & post request for property update view as logged in landlord user"""
        prop = sampleProperty()
        prop1 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('user'), self.landlord)
        self.assertEqual(response.context.get('object'), prop)

        response = self.client.post(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}), 
                    data={'title': "new property", 'fromDate': datetime.date.today(), 
                            'toDate':datetime.date.today(), 'propertyimage_set-TOTAL_FORMS': 4,
                            'propertyimage_set-INITIAL_FORMS': 4, 'propertyimage_set-MAX_NUM_FORMS': 10,
                            'propertyvideo_set-TOTAL_FORMS': 1, 'propertyvideo_set-INITIAL_FORMS': 1, 
                            'propertyvideo_set-MAX_NUM_FORMS': 4
                        }
                )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(prop.title, 'new property')

        response = self.client.get(reverse('property:propertyUpdate', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        response = self.client.post(reverse('property:propertyUpdate', kwargs={'slug': prop1.urlSlug}), 
                    data={'title': "new property", 'fromDate': datetime.date.today(), 
                            'toDate':datetime.date.today(), 'propertyimage_set-TOTAL_FORMS': 4,
                            'propertyimage_set-INITIAL_FORMS': 4, 'propertyimage_set-MAX_NUM_FORMS': 10,
                            'propertyvideo_set-TOTAL_FORMS': 1, 'propertyvideo_set-INITIAL_FORMS': 1, 
                            'propertyvideo_set-MAX_NUM_FORMS': 4
                        }
                )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_property_delete_landlord_access(self):
        """
        Test get & post request for property delete view as logged in landlord user and
        Testing get & post of other landlord property deletion failed & success url
        """
        prop = sampleProperty()
        prop1 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('user'), self.landlord)
        self.assertEqual(response.context.get('object'), prop)
        self.assertTrue(propmodel.Property.objects.filter(urlSlug=prop.urlSlug).exists())

        response = self.client.post(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        self.assertFalse(propmodel.Property.objects.filter(urlSlug=prop.urlSlug).exists())

        response = self.client.get(reverse('property:propertyDelete', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        response = self.client.post(reverse('property:propertyDelete', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(propmodel.Property.objects.filter(urlSlug=prop1.urlSlug).exists())

    def test_landlord_property_manage_access(self):
        """Test get & post request for landlord manage property view as logged in landlord user"""
        prop = sampleProperty()
        prop1 = sampleProperty()
        prop2 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('user'), self.landlord)
        self.assertEqual(response.context.get('object_list').count(), 2)
        self.assertEqual(str(response.context.get('object_list')), f"<QuerySet [<Property: {prop}>, <Property: {prop1}>]>")

        response = self.client.post(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_property_list_view_access_landlord(self):
        """
        Test get & post request for property list view as logged in landlord user.
        He should not be allowed access
        """
        response = self.client.get(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = self.client.post(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_property_detail_view_access_landlord(self):
        """
        Test get & post request for property detail view as logged in landlord user.
        He should not be allowed to access other property which he is not created
        """
        prop1 = sampleProperty()
        prop2 = sampleProperty(landName="LandlordUser")
        # his property access
        response = self.client.get(reverse('property:propertyDetail', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object'), prop1)

        response = self.client.post(reverse('property:propertyDetail', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        #other property should not be accessed
        response = self.client.get(reverse('property:propertyDetail', kwargs={'slug': prop2.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(reverse('property:propertyDetail', kwargs={'slug': prop2.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_property_like_dislike_view_access_landlord(self):
        """
        Test get & post request for like & dislike as logged in landlord user.
        He should not be allowed to like or dislike
        """
        prop1 = sampleProperty()
        response = self.client.get(reverse('property:propertyReaction', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_property_post_question_view_access_landlord(self):
        """
        Test get & post request for post question as logged in landlord user.
        He should not be allowed to post question
        """
        prop1 = sampleProperty()
        response = self.client.get(reverse('property:propertyQuestion', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(reverse('property:propertyQuestion', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_property_post_answer_view_access_landlord(self):
        """
        Test get & post request for post answer as logged in landlord user.
        He should be allowed to post answer
        """
        prop1 = sampleProperty()
        stud = createStudentUser(username="StudentUser")
        studObject = models.UserStudent.objects.get(user__user=stud)
        q1 = propmodel.PostQuestion.objects.create(propKey=prop1, question="What is the amount of rent?", student=studObject)
        response = self.client.get(reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': q1.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop1.urlSlug))

        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': q1.pk}),
                        data={'prop-answer': "Per month $1000"}
                    )
        answer = propmodel.PostAnswer.objects.get(question=q1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop1.urlSlug))
        self.assertEqual(answer.answer, "Per month $1000")

        #invalid Requests
        response = self.client.get(reverse('property:propertyAnswer', kwargs={'slug': "sad-sad", 'pk': q1.pk}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': "sad-sad", 'pk': q1.pk}),
                        data={'prop-answer': "Per month $1000"}
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        prop2 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyAnswer', kwargs={'slug': prop2.urlSlug, 'pk': q1.pk}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': prop2.urlSlug, 'pk': q1.pk}),
                        data={'prop-answer': "Per month $1000"}
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': 20}),
                        data={'prop-answer': 4234}
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': q1.pk}),
                        data={'prop-answer': ""}
                    )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop1.urlSlug))
        self.assertEqual(propmodel.PostAnswer.objects.filter(question=q1).count(), 1)


class PrivateStudentAccessTests(TestCase):
    """
    Test View request that require authentication of Student and view request that should
    not be accessed by Student.
    """
    def setUp(self):
        self.student = createStudentUser()
        self.client = client
        self.client.force_login(user=self.student)

    def test_property_create_student_access(self):
        """Test get & post request for property create view as logged in student user"""

        response = self.client.get(reverse('property:propertyCreate'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = self.client.post(reverse('property:propertyCreate'), 
                    data={'title': "new property", 'fromDate': datetime.date.today(), 
                            'toDate':datetime.date.today(), 'propertyimage_set-TOTAL_FORMS': 4,
                            'propertyimage_set-INITIAL_FORMS': 4, 'propertyimage_set-MAX_NUM_FORMS': 10,
                            'propertyvideo_set-TOTAL_FORMS': 1, 'propertyvideo_set-INITIAL_FORMS': 1, 
                            'propertyvideo_set-MAX_NUM_FORMS': 4
                        }
                )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(propmodel.Property.objects.filter(urlSlug="new-property").exists())

    def test_property_update_student_access(self):
        """Test get & post request for property update view as logged in student user"""

        prop = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}), 
                    data={'title': "new property", 'fromDate': datetime.date.today(), 
                            'toDate':datetime.date.today(), 'propertyimage_set-TOTAL_FORMS': 4,
                            'propertyimage_set-INITIAL_FORMS': 4, 'propertyimage_set-MAX_NUM_FORMS': 10,
                            'propertyvideo_set-TOTAL_FORMS': 1, 'propertyvideo_set-INITIAL_FORMS': 1, 
                            'propertyvideo_set-MAX_NUM_FORMS': 4
                        }
                )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_property_delete_student_access(self):
        """
        Test get & post request for property delete view as logged in student user.
        He should not be allowed.
        """
        prop = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(propmodel.Property.objects.filter(urlSlug=prop.urlSlug).exists())

        response = self.client.post(reverse('property:propertyDelete', kwargs={'slug': prop.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(propmodel.Property.objects.filter(urlSlug=prop.urlSlug).exists())

    def test_landlord_property_manage_student_access(self):
        """Test get & post request for landlord manage property view as logged in student user"""
        
        response = self.client.get(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = self.client.post(reverse('property:propertyManage'))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_property_list_view_access_student(self):
        """
        Test get & post request for property list view as logged in student user.
        """
        response = self.client.get(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 0)

        response = self.client.post(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_property_detail_view_access_student(self):
        """
        Test get & post request for property detail view as logged in student user.
        """
        prop1 = sampleProperty(landName="LandlordUser1")
        prop2 = sampleProperty(landName="LandlordUser")

        response = self.client.get(reverse('property:propertyDetail', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object'), prop1)

        response = self.client.get(reverse('property:propertyDetail', kwargs={'slug': prop2.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object'), prop2)

        response = self.client.post(reverse('property:propertyDetail', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_property_like_dislike_view_access_student(self):
        """
        Test get & post request for like & dislike as logged in student user.
        He should be allowed to like or dislike
        """
        prop1 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyReaction', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/')

        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop1.urlSlug}),
                        data={'like': 1, 'dislike': 1}
                    )
        data = response.json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(data.get('liked'), 1)
        self.assertEqual(data.get('disliked'), 0)
        self.assertEqual(data.get('likecount'), prop1.totalLikes())
        self.assertEqual(data.get('dislikecount'), prop1.totalDislikes())

    def test_property_post_question_view_access_student(self):
        """
        Test get & post request for post question as logged in student user.
        He should be allowed to post question
        """
        prop1 = sampleProperty(landName="LandlordUser")
        response = self.client.get(reverse('property:propertyQuestion', kwargs={'slug': prop1.urlSlug}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/{}/'.format(prop1.urlSlug))

        response = self.client.post(reverse('property:propertyQuestion', kwargs={'slug': prop1.urlSlug}),
                        data={'question': "Does the house has good Air flow?"}
                    )
        data = response.json()
        ques = propmodel.PostQuestion.objects.get(propKey=prop1)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(data.get('question'), "Does the house has good Air flow?")
        self.assertEqual(data.get('question'), ques.question)

        # invalid requests
        response = self.client.get(reverse('property:propertyQuestion', kwargs={'slug': "ada-asdas"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/property/ada-asdas/')

        response = self.client.post(reverse('property:propertyQuestion', kwargs={'slug': "ada-asdas"}),
                        data={'question': 12132}
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(reverse('property:propertyQuestion', kwargs={'slug': "ada-asdas"}),
                        data={'question': ''}
                    )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json().get('question'), '')
        self.assertEqual(propmodel.PostQuestion.objects.filter(propKey=prop1).count(), 1)    

    def test_property_post_answer_view_access_student(self):
        """
        Test get & post request for post answer as logged in student user.
        He should not be allowed to post answer
        """
        prop1 = sampleProperty(landName="LandlordUser")
        studObject = models.UserStudent.objects.get(user__user=self.student)
        q1 = propmodel.PostQuestion.objects.create(propKey=prop1, question="Is there 24hrs WIFI?", student=studObject)

        response = self.client.get(reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': q1.pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(
                        reverse('property:propertyAnswer', kwargs={'slug': prop1.urlSlug, 'pk': q1.pk}),
                        data={'prop-answer': "Yes we have"}
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertFalse(propmodel.PostAnswer.objects.filter(question=q1).exists())


class PropertyCreateUpdateViewFieldsTests(TestCase):
    """ 
    Test Module for Post request form data for property create & update view by logged 
    in landlord user
    """

    def setUp(self):
        
        self.landlord = createLandlordUser()
        self.client = client
        self.client.force_login(user=self.landlord)
        self.validPayload1 = {'title': "New Property Near Lake", 'city': city().pk, 'zipcode': 12345,
                                'address': "address of property", 'sqft': 123, 'occupants': 10,
                                'rooms': 15, 'bathrooms': 5, 'securityDeposit': True, 'amount': 10000,
                                'rentPerPerson': 1000, 'description': "Description", 'utilities': True,
                                'garage': True, 'parkingSpace': 10, 
                                'amenities': [amenity().pk, amenity(name="Pool").pk],
                                'fromDate': datetime.date.today(), 
                                'toDate': datetime.date.today() + datetime.timedelta(days=1),
                                'propertyimage_set-TOTAL_FORMS': 10, 
                                'propertyimage_set-INITIAL_FORMS': 0, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyimage_set-0-imageDescription': 'bathroom',
                                'propertyimage_set-0-imagePath': MockImageVideo(),
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': MockImageVideo(),
                                'propertyimage_set-2-imageDescription': 'hall',
                                'propertyimage_set-2-imagePath': MockImageVideo(),
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': MockImageVideo(),
                                'propertyimage_set-4-imageDescription': 'room2',
                                'propertyimage_set-4-imagePath': MockImageVideo(),
                                'propertyimage_set-5-imageDescription': 'room3',
                                'propertyimage_set-5-imagePath': MockImageVideo(),
                                'propertyimage_set-6-imageDescription': 'room4',
                                'propertyimage_set-6-imagePath': MockImageVideo(),
                                'propertyimage_set-7-imageDescription': 'room5',
                                'propertyimage_set-7-imagePath': MockImageVideo(),
                                'propertyimage_set-8-imageDescription': 'room6',
                                'propertyimage_set-8-imagePath': MockImageVideo(),
                                'propertyimage_set-9-imageDescription': 'room7',
                                'propertyimage_set-9-imagePath': MockImageVideo(),
                                'propertyvideo_set-TOTAL_FORMS': 4, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.mp4'),
                                'propertyvideo_set-1-videoDescription': 'room1',
                                'propertyvideo_set-1-videoPath': MockImageVideo('.avi'),
                                'propertyvideo_set-2-videoDescription': 'hall2',
                                'propertyvideo_set-2-videoPath': MockImageVideo('.mov'),
                                'propertyvideo_set-3-videoDescription': 'room2',
                                'propertyvideo_set-3-videoPath': MockImageVideo('.mkv'),
                            }
        # self.validPayload2 - 4 image & 1 video
        # self.invalidPayload1 - no field value
        # self.invalidPayload2 - wrong value

    def test_create_property_view_valid_payload1(self):
        """ Test creating new property with valid all fields payload1 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload1
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')
        self.assertEqual(prop.landlord.user.user, self.landlord)
        self.assertEqual(prop.title, self.validPayload1.get('title'))
        self.assertEqual(prop.zipcode, str(self.validPayload1.get('zipcode')))
        self.assertEqual(prop.urlSlug, "new-property-near-lake")
        self.assertEqual(prop.city.pk, self.validPayload1.get('city'))
        self.assertEqual(prop.rooms, self.validPayload1.get('rooms'))
        self.assertEqual(prop.securityDeposit, self.validPayload1.get('securityDeposit'))
        self.assertEqual(prop.amount, self.validPayload1.get('amount'))
        self.assertEqual(prop.fromDate, self.validPayload1.get('fromDate'))
        self.assertEqual(prop.toDate, self.validPayload1.get('toDate'))
        self.assertEqual(prop.totalLikes(), 0)
        self.assertEqual(prop.totalDislikes(), 0)
        self.assertEqual(prop.propertyimage_set.count(), 10)
        self.assertEqual(prop.propertyvideo_set.count(), 4)

        prop.delete()

