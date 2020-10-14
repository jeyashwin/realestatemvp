from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from PIL import Image
import datetime, tempfile

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
        self.validPayload2 = {'title': "New Property Near Lake", 'city': city().pk, 'zipcode': "54353",
                                'address': "address of property", 'sqft': 123, 'occupants': 10,
                                'rooms': 15, 'bathrooms': 5, 'securityDeposit': False, 'amount': 10000,
                                'rentPerPerson': 1000, 'description': "Description",
                                'amenities': [amenity().pk, amenity(name="Pool").pk],
                                'fromDate': datetime.date.today(), 
                                'toDate': datetime.date.today() + datetime.timedelta(days=1),
                                'propertyimage_set-TOTAL_FORMS': 5, 
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
                                'propertyimage_set-4-imageDescription': 'room1',
                                'propertyimage_set-4-imagePath': MockImageVideo(),
                                'propertyimage_set-4-DELETE': 'True',
                                'propertyvideo_set-TOTAL_FORMS': 2, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.mp4'),
                                'propertyvideo_set-1-videoDescription': 'room4',
                                'propertyvideo_set-1-videoPath': MockImageVideo('.mp4'),
                                'propertyvideo_set-1-DELETE': 'True',
                            }
        self.invalidPayload1 = {'title': "", 'city': '', 'zipcode': '', 'address': '', 'sqft': '', 
                                'occupants': '', 'rooms': '', 'bathrooms': '', 'securityDeposit': True, 
                                'amount': '', 'rentPerPerson': '', 'description': '', 'amenities': [],
                                'fromDate': '', 'toDate': '',
                                'propertyimage_set-TOTAL_FORMS': 4, 
                                'propertyimage_set-INITIAL_FORMS': 0, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyimage_set-0-imageDescription': '',
                                'propertyimage_set-0-imagePath': MockImageVideo(),
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': '',
                                'propertyimage_set-2-imageDescription': '',
                                'propertyimage_set-2-imagePath': '',
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': '',
                                'propertyvideo_set-TOTAL_FORMS': 3, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': '',
                                'propertyvideo_set-0-videoPath': '',
                                'propertyvideo_set-1-videoDescription': 'room4',
                                'propertyvideo_set-1-videoPath': '',
                                'propertyvideo_set-2-videoDescription': '',
                                'propertyvideo_set-2-videoPath': MockImageVideo('.mp4'),
                            }
        self.invalidPayload2 = {'title': "New Property Near Lake", 'city': 12, 'zipcode': "1qw15",
                                'address': "address of property", 'sqft': -10, 'occupants': -5,
                                'rooms': 0, 'bathrooms': -2, 'securityDeposit': True, 'amount': -1000,
                                'rentPerPerson': -2000, 'description': "Description", 'utilities': '23',
                                'garage': '23', 'parkingSpace': -50, 'amenities': [234],
                                'fromDate': '202asas', 'toDate': '4324324dsfds',
                                'propertyimage_set-TOTAL_FORMS': 6, 
                                'propertyimage_set-INITIAL_FORMS': 0, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyimage_set-0-imageDescription': 'bathroom',
                                'propertyimage_set-0-imagePath': MockImageVideo('.mp4'),
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': MockImageVideo(),
                                'propertyimage_set-2-imageDescription': 'hall',
                                'propertyimage_set-2-imagePath': MockImageVideo(),
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': MockImageVideo(),
                                'propertyimage_set-4-imageDescription': 'room2',
                                'propertyimage_set-4-imagePath': MockImageVideo(),
                                'propertyimage_set-5-imageDescription': 'room3',
                                'propertyimage_set-5-imagePath': MockImageVideo('.mov'),
                                'propertyvideo_set-TOTAL_FORMS': 3, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.jpg'),
                                'propertyvideo_set-1-videoDescription': 'room1',
                                'propertyvideo_set-1-videoPath': MockImageVideo('.avi'),
                                'propertyvideo_set-2-videoDescription': 'hall2',
                                'propertyvideo_set-2-videoPath': MockImageVideo('.pdf'),
                            }
        self.invalidPayload3 = {'title': "New Property Near Lake", 'city': 100, 'zipcode': "115",
                                'address': "address of property", 'sqft': 1000, 'occupants': 21,
                                'rooms': 30, 'bathrooms': 43, 'securityDeposit': True, 'amount': 0,
                                'rentPerPerson': 0, 'description': "Description", 'utilities': '23',
                                'garage': '23', 'parkingSpace': 65, 'amenities': [234],
                                'fromDate': datetime.date.today() - datetime.timedelta(days=1), 
                                'toDate': datetime.date.today() - datetime.timedelta(days=1),
                                'propertyimage_set-TOTAL_FORMS': 4, 
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
                                'propertyvideo_set-TOTAL_FORMS': 1, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.mov'),
                            }
        self.validUpdatePayload1 = {'title': "Lake Property", 'city': city().pk, 'zipcode': 32534,
                                'address': "property address", 'sqft': 3203, 'occupants': 3,
                                'rooms': 5, 'bathrooms': 2, 'securityDeposit': False, 'amount': 10000,
                                'rentPerPerson': 500, 'description': "Description", 'utilities': False,
                                'garage': False, 'parkingSpace': 1, 
                                'amenities': [amenity(name="Heater").pk, amenity(name="Gym").pk],
                                'fromDate': datetime.date.today(), 
                                'toDate': datetime.date.today() + datetime.timedelta(days=30),
                                'propertyimage_set-TOTAL_FORMS': 8, 
                                'propertyimage_set-INITIAL_FORMS': 10, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                # 'propertyimage_set-0-propertyKey': 4,
                                'propertyimage_set-0-imageDescription': 'bathroom',
                                'propertyimage_set-0-imagePath': MockImageVideo(),
                                'propertyimage_set-0-DELETE': True,
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': MockImageVideo(),
                                'propertyimage_set-2-imageDescription': 'hall',
                                'propertyimage_set-2-imagePath': MockImageVideo('.jpg'),
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': MockImageVideo(),
                                'propertyimage_set-4-imageDescription': 'room2',
                                'propertyimage_set-4-imagePath': MockImageVideo(),
                                'propertyimage_set-5-imageDescription': 'room3',
                                'propertyimage_set-5-imagePath': MockImageVideo(),
                                'propertyimage_set-5-DELETE': True,
                                'propertyimage_set-6-imageDescription': 'room4',
                                'propertyimage_set-6-imagePath': MockImageVideo(),
                                'propertyimage_set-7-imageDescription': 'room5',
                                'propertyimage_set-7-imagePath': MockImageVideo(),
                                'propertyimage_set-8-imageDescription': 'room6',
                                'propertyimage_set-8-imagePath': MockImageVideo(),
                                'propertyimage_set-9-imageDescription': 'room7',
                                'propertyimage_set-9-imagePath': MockImageVideo(),
                                'propertyvideo_set-TOTAL_FORMS': 3, 
                                'propertyvideo_set-INITIAL_FORMS': 4, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.mp4'),
                                'propertyvideo_set-1-videoDescription': 'room1',
                                'propertyvideo_set-1-videoPath': MockImageVideo('.avi'),
                                'propertyvideo_set-1-DELETE': 'True',
                                'propertyvideo_set-2-videoDescription': 'hall2',
                                'propertyvideo_set-2-videoPath': MockImageVideo('.mov'),
                                'propertyvideo_set-3-videoDescription': 'room2',
                                'propertyvideo_set-3-videoPath': MockImageVideo('.mkv'),
                            }
        self.validUpdatePayload2 = {'title': "lake property", 'city': city().pk, 'zipcode': "54353",
                                'address': "address of property", 'sqft': 123, 'occupants': 10,
                                'rooms': 15, 'bathrooms': 5, 'securityDeposit': False, 'amount': 10000,
                                'rentPerPerson': 1000, 'description': "Description",
                                'amenities': [amenity().pk, amenity(name="Pool").pk],
                                'fromDate': datetime.date.today(), 
                                'toDate': datetime.date.today() + datetime.timedelta(days=1),
                                'propertyimage_set-TOTAL_FORMS': 3, 
                                'propertyimage_set-INITIAL_FORMS': 4, 
                                'propertyimage_set-MIN_NUM_FORMS': 4,
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyimage_set-0-imageDescription': 'bathroom',
                                'propertyimage_set-0-imagePath': MockImageVideo(),
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': MockImageVideo(),
                                'propertyimage_set-2-imageDescription': 'hall',
                                'propertyimage_set-2-imagePath': MockImageVideo(),
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': MockImageVideo(),
                                'propertyimage_set-3-DELETE': True,
                                'propertyvideo_set-TOTAL_FORMS': 0, 
                                'propertyvideo_set-INITIAL_FORMS': 1,
                                'propertyvideo_set-MIN_NUM_FORMS': 1,
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': 'room4',
                                'propertyvideo_set-0-videoPath': MockImageVideo('.mp4'),
                                'propertyvideo_set-0-DELETE': 'True',
                            }
        self.invalidUpdatePayload1 = {'title': "", 'city': '', 'zipcode': '', 'address': '', 'sqft': '', 
                                'occupants': '', 'rooms': '', 'bathrooms': '', 'securityDeposit': True, 
                                'amount': '', 'rentPerPerson': '', 'description': '', 'amenities': [],
                                'fromDate': '', 'toDate': '',
                                'propertyimage_set-TOTAL_FORMS': 4, 
                                'propertyimage_set-INITIAL_FORMS': 4, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyimage_set-0-imageDescription': '',
                                'propertyimage_set-0-imagePath': MockImageVideo(),
                                'propertyimage_set-1-imageDescription': 'bedroom',
                                'propertyimage_set-1-imagePath': '',
                                'propertyimage_set-2-imageDescription': '',
                                'propertyimage_set-2-imagePath': '',
                                'propertyimage_set-3-imageDescription': 'room1',
                                'propertyimage_set-3-imagePath': '',
                                'propertyvideo_set-TOTAL_FORMS': 3, 
                                'propertyvideo_set-INITIAL_FORMS': 3, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                                'propertyvideo_set-0-videoDescription': '',
                                'propertyvideo_set-0-videoPath': '',
                                'propertyvideo_set-1-videoDescription': 'room4',
                                'propertyvideo_set-1-videoPath': '',
                                'propertyvideo_set-2-videoDescription': '',
                                'propertyvideo_set-2-videoPath': MockImageVideo('.mp4'),
                            }
        self.invalidUpdatePayload2 = {
                                'fromDate': datetime.date.today() - datetime.timedelta(days=2),
                                'toDate': datetime.date.today() - datetime.timedelta(days=3),
                                'propertyimage_set-TOTAL_FORMS': 4, 
                                'propertyimage_set-INITIAL_FORMS': 0, 
                                'propertyimage_set-MAX_NUM_FORMS': 10,
                                'propertyvideo_set-TOTAL_FORMS': 1, 
                                'propertyvideo_set-INITIAL_FORMS': 0, 
                                'propertyvideo_set-MAX_NUM_FORMS': 4,
                            }

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

    def test_create_property_view_valid_minimum_payload2(self):
        """ Test creating new property with valid all fields minimum payload2 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload2
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')
        self.assertEqual(prop.landlord.user.user, self.landlord)
        self.assertEqual(prop.title, self.validPayload2.get('title'))
        self.assertEqual(prop.zipcode, str(self.validPayload2.get('zipcode')))
        self.assertEqual(prop.urlSlug, "new-property-near-lake")
        self.assertEqual(prop.city.pk, self.validPayload2.get('city'))
        self.assertEqual(prop.rooms, self.validPayload2.get('rooms'))
        self.assertFalse(prop.securityDeposit)
        self.assertEqual(prop.amount, None)
        self.assertEqual(prop.fromDate, self.validPayload2.get('fromDate'))
        self.assertEqual(prop.toDate, self.validPayload2.get('toDate'))
        self.assertEqual(prop.totalLikes(), 0)
        self.assertEqual(prop.totalDislikes(), 0)
        self.assertEqual(prop.propertyimage_set.count(), 4)
        self.assertEqual(prop.propertyvideo_set.count(), 1)

        prop.delete()

    def test_create_property_view_invalid_payload1(self):
        """ Test creating new property with invalid fields payload1 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.invalidPayload1
        )
        errorForm = response.context.get('form').errors
        errorImageForm = response.context.get('imageForm').errors
        errorVideoForm = response.context.get('videoForm').errors

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(propmodel.Property.objects.filter(landlord__user__user=self.landlord).count(), 0)
        self.assertEqual(errorForm.get("title"), ['This field is required.'])
        self.assertEqual(errorForm.get("city"), ['This field is required.'])
        self.assertEqual(errorForm.get("zipcode"), ['This field is required.'])
        self.assertEqual(errorForm.get("address"), ['This field is required.'])
        self.assertEqual(errorForm.get("sqft"), ['This field is required.'])
        self.assertEqual(errorForm.get("occupants"), ['This field is required.'])
        self.assertEqual(errorForm.get("rooms"), ['This field is required.'])
        self.assertEqual(errorForm.get("bathrooms"), ['This field is required.'])
        self.assertEqual(errorForm.get("amount"), ['This field is required.'])
        self.assertEqual(errorForm.get("rentPerPerson"), ['This field is required.'])
        self.assertEqual(errorForm.get("description"), ['This field is required.'])
        self.assertEqual(errorForm.get("amenities"), ['This field is required.'])
        self.assertEqual(errorForm.get("fromDate"), ['This field is required.'])
        self.assertEqual(errorForm.get("toDate"), ['This field is required.'])

        self.assertEqual(errorImageForm[0].get("imageDescription"), ['This field is required.'])
        self.assertEqual(errorImageForm[1].get("imagePath"), ['This field is required.'])
        self.assertEqual(errorImageForm[2].get("imageDescription"), ['This field is required.'])
        self.assertEqual(errorImageForm[2].get("imagePath"), ['This field is required.'])
        self.assertEqual(errorImageForm[3].get("imagePath"), ['This field is required.'])
        self.assertEqual(errorVideoForm[0].get("videoDescription"), ['This field is required.'])
        self.assertEqual(errorVideoForm[0].get("videoPath"), ['This field is required.', "File extension '' is not allowed. Allowed extensions are: ['mov', 'mp4', 'avi', 'mkv']."])
        self.assertEqual(errorVideoForm[1].get("videoPath"), ['This field is required.', "File extension '' is not allowed. Allowed extensions are: ['mov', 'mp4', 'avi', 'mkv']."])
        self.assertEqual(errorVideoForm[2].get("videoDescription"), ['This field is required.'])

    def test_create_property_view_invalid_payload2(self):
        """ Test creating new property with invalid fields payload2 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.invalidPayload2
        )
        errorForm = response.context.get('form').errors
        errorImageForm = response.context.get('imageForm').errors
        errorVideoForm = response.context.get('videoForm').errors

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(propmodel.Property.objects.filter(landlord__user__user=self.landlord).count(), 0)
        self.assertEqual(errorForm.get("city"), ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(errorForm.get("zipcode"), ['Only numbers allowed.'])
        self.assertEqual(errorForm.get("sqft"), ['Square Feet should be atleast 1.'])
        self.assertEqual(errorForm.get("occupants"), ['Minimum 1'])
        self.assertEqual(errorForm.get("rooms"), ['Minimum 1'])
        self.assertEqual(errorForm.get("bathrooms"), ['Minimum 1'])
        self.assertEqual(errorForm.get("amount"), ['Minimum Amount cannot be lower than 0'])
        self.assertEqual(errorForm.get("rentPerPerson"), ['Minimum Price cannot be lower than 0'])
        self.assertEqual(errorForm.get("parkingSpace"), ['Minimum 0'])
        self.assertEqual(errorForm.get("amenities"), ['Select a valid choice. 234 is not one of the available choices.'])
        self.assertEqual(errorForm.get("fromDate"), ['Enter a valid date.'])
        self.assertEqual(errorForm.get("toDate"), ['Enter a valid date.'])

        self.assertEqual(errorImageForm[0].get("imagePath"), ["File extension 'mp4' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])
        self.assertEqual(errorImageForm[5].get("imagePath"), ["File extension 'mov' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])
        self.assertEqual(errorVideoForm[0].get("videoPath"), ["File extension 'jpg' is not allowed. Allowed extensions are: ['mov', 'mp4', 'avi', 'mkv']."])
        self.assertEqual(errorVideoForm[2].get("videoPath"), ["File extension 'pdf' is not allowed. Allowed extensions are: ['mov', 'mp4', 'avi', 'mkv']."])

    def test_create_property_view_invalid_payload3(self):
        """ Test creating new property with invalid fields payload3 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.invalidPayload3
        )
        errorForm = response.context.get('form').errors
        errorImageForm = response.context.get('imageForm').errors
        errorVideoForm = response.context.get('videoForm').errors
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(propmodel.Property.objects.filter(landlord__user__user=self.landlord).count(), 0)
        self.assertEqual(errorForm.get("city"), ['Select a valid choice. That choice is not one of the available choices.'])
        self.assertEqual(errorForm.get("zipcode"), ['Only numbers allowed.', '5 digit code'])
        self.assertEqual(errorForm.get("occupants"), ['Maximum 20'])
        self.assertEqual(errorForm.get("rooms"), ['Maximum 20'])
        self.assertEqual(errorForm.get("bathrooms"), ['Maximum 20'])
        self.assertEqual(errorForm.get("amount"), None)
        self.assertEqual(errorForm.get("rentPerPerson"), None)
        self.assertEqual(errorForm.get("parkingSpace"), ['Maximum 20'])
        self.assertEqual(errorForm.get("amenities"), ['Select a valid choice. 234 is not one of the available choices.'])
        self.assertEqual(errorForm.get("fromDate"), ['From Date cannot be older than today.'])
        self.assertEqual(errorForm.get("toDate"), ['To Date cannot be less than or equal to From Date.'])

    def test_update_property_view_valid_payload1(self):
        """ Test updating property with valid all fields payload1 """
        response1 = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload1
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        img1 = propmodel.PropertyImage.objects.get(propertyKey=prop, imageDescription=self.validUpdatePayload1.get("propertyimage_set-0-imageDescription"))
        img2 = propmodel.PropertyImage.objects.get(propertyKey=prop, imageDescription=self.validUpdatePayload1.get("propertyimage_set-5-imageDescription"))
        vid1 = propmodel.PropertyVideo.objects.get(propertyKey=prop, videoDescription=self.validUpdatePayload1.get("propertyvideo_set-1-videoDescription"))
        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertEqual(response1.url, '/myproperty/')
        self.assertTrue(propmodel.PropertyImage.objects.filter(pk=img1.pk).exists())
        self.assertTrue(propmodel.PropertyImage.objects.filter(pk=img2.pk).exists())
        self.assertTrue(propmodel.PropertyVideo.objects.filter(pk=vid1.pk).exists())

        for j, i in enumerate(prop.propertyimage_set.all()):
            self.validUpdatePayload1[f'propertyimage_set-{j}-id']= i.pk
        
        for j, i in enumerate(prop.propertyvideo_set.all()):
            self.validUpdatePayload1[f'propertyvideo_set-{j}-id']= i.pk

        response = self.client.post(
            reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}),
            data=self.validUpdatePayload1
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')
        
        prop.refresh_from_db()

        self.assertEqual(prop.landlord.user.user, self.landlord)
        self.assertEqual(prop.title, self.validUpdatePayload1.get('title'))
        self.assertEqual(prop.zipcode, str(self.validUpdatePayload1.get('zipcode')))
        self.assertEqual(prop.urlSlug, "lake-property")
        self.assertEqual(prop.rooms, self.validUpdatePayload1.get('rooms'))
        self.assertFalse(prop.securityDeposit)
        self.assertEqual(prop.amount, None)
        self.assertEqual(prop.fromDate, self.validUpdatePayload1.get('fromDate'))
        self.assertEqual(prop.toDate, self.validUpdatePayload1.get('toDate'))
        self.assertEqual(prop.totalLikes(), 0)
        self.assertEqual(prop.totalDislikes(), 0)
        self.assertEqual(prop.propertyimage_set.count(), 8)
        self.assertEqual(prop.propertyvideo_set.count(), 3)
        self.assertFalse(propmodel.PropertyImage.objects.filter(pk=img1.pk).exists())
        self.assertFalse(propmodel.PropertyImage.objects.filter(pk=img2.pk).exists())
        self.assertFalse(propmodel.PropertyVideo.objects.filter(pk=vid1.pk).exists())

        prop.delete()

    def test_update_property_view_valid_minimum_payload2(self):
        """ Test update property with valid all fields minimum payload2 """
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload2
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')

        for j, i in enumerate(prop.propertyimage_set.all()):
            self.validUpdatePayload2[f'propertyimage_set-{j}-id']= i.pk
        
        for j, i in enumerate(prop.propertyvideo_set.all()):
            self.validUpdatePayload2[f'propertyvideo_set-{j}-id']= i.pk

        response = self.client.post(
            reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}),
            data=self.validUpdatePayload2
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        prop.refresh_from_db()
        self.assertEqual(prop.landlord.user.user, self.landlord)
        self.assertEqual(prop.title, self.validUpdatePayload2.get('title'))
        
        self.assertEqual(prop.propertyimage_set.count(), 4)
        self.assertEqual(prop.propertyvideo_set.count(), 1)

        prop.delete()

    def test_update_property_view_invalid_payload1(self):
        """ Test update property with invalid fields payload1 """
        self.validPayload2['propertyvideo_set-2-videoDescription'] = 'room4'
        self.validPayload2['propertyvideo_set-2-videoPath'] = MockImageVideo('.mp4')
        self.validPayload2['propertyvideo_set-3-videoDescription'] = 'room4'
        self.validPayload2['propertyvideo_set-3-videoPath'] = MockImageVideo('.mp4')
        
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload2
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')

        for j, i in enumerate(prop.propertyimage_set.all()):
            self.invalidUpdatePayload1[f'propertyimage_set-{j}-id']= i.pk
        
        for j, i in enumerate(prop.propertyvideo_set.all()):
            self.invalidUpdatePayload1[f'propertyvideo_set-{j}-id']= i.pk

        response = self.client.post(
            reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}),
            data=self.invalidUpdatePayload1
        )
        errorForm = response.context.get('form').errors
        errorImageForm = response.context.get('imageForm').errors
        errorVideoForm = response.context.get('videoForm').errors


        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(errorForm.get("title"), ['This field is required.'])
        self.assertEqual(errorForm.get("city"), ['This field is required.'])
        self.assertEqual(errorForm.get("zipcode"), ['This field is required.'])
        self.assertEqual(errorForm.get("address"), ['This field is required.'])
        self.assertEqual(errorForm.get("sqft"), ['This field is required.'])
        self.assertEqual(errorForm.get("occupants"), ['This field is required.'])
        self.assertEqual(errorForm.get("rooms"), ['This field is required.'])
        self.assertEqual(errorForm.get("bathrooms"), ['This field is required.'])
        self.assertEqual(errorForm.get("amount"), ['This field is required.'])
        self.assertEqual(errorForm.get("rentPerPerson"), ['This field is required.'])
        self.assertEqual(errorForm.get("description"), ['This field is required.'])
        self.assertEqual(errorForm.get("amenities"), ['This field is required.'])
        self.assertEqual(errorForm.get("fromDate"), ['This field is required.'])
        self.assertEqual(errorForm.get("toDate"), ['This field is required.'])

        self.assertEqual(errorImageForm[0].get("imageDescription"), ['This field is required.'])
        self.assertEqual(errorImageForm[2].get("imageDescription"), ['This field is required.'])
        self.assertEqual(errorVideoForm[0].get("videoDescription"), ['This field is required.'])
        self.assertEqual(errorVideoForm[2].get("videoDescription"), ['This field is required.'])

        prop.delete()

    def test_update_property_view_invalid_payload2(self):
        """ Test update property with invalid fields payload2 """
        
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload2
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')

        response = self.client.post(
            reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}),
            data={}
        )
        # print(response.context.get('forms').errors)
        fromDate = prop.fromDate
        toDate = prop.toDate
        prop.refresh_from_db()
        self.assertEqual(fromDate, prop.fromDate)
        self.assertEqual(toDate, prop.toDate)

        prop.delete()
    
    def test_update_property_view_invalid_payload3(self):
        """ Test update property with invalid fields payload3 """
        
        response = self.client.post(
            reverse('property:propertyCreate'),
            data=self.validPayload2
        )
        prop = propmodel.Property.objects.get(landlord__user__user=self.landlord)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/myproperty/')

        response = self.client.post(
            reverse('property:propertyUpdate', kwargs={'slug': prop.urlSlug}),
            data=self.invalidUpdatePayload2
        )
        self.assertEqual(response.context.get('form').errors.get("fromDate"), ['From Date cannot be older than today.'])
        self.assertEqual(response.context.get('form').errors.get("toDate"), ['To Date cannot be less than or equal to From Date.'])

        prop.delete()


def samplePropertyList(landName=None, room=1, bath=6, occp=10, rent=2000, sqft=1000, amenty=None):
    if landName is None:
        landlord = createLandlordUser()
    else:
        landlord = createLandlordUser(username=landName)
    landlordObject = models.UserLandLord.objects.get(user__user=landlord)
    prop = propmodel.Property.objects.create(landlord=landlordObject, title="New property near lake", 
            city=city(), zipcode=12345, address="10/2 North cross", sqft=sqft, occupants=occp, rooms=room,
            bathrooms=bath, securityDeposit=True, amount=1000, rentPerPerson=rent, 
            description="asdas asdas", utilities=True, garage=True, parkingSpace=10, 
            fromDate=datetime.date.today(), toDate=datetime.date.today() + datetime.timedelta(days=2)
        )
    prop.amenities.set(amenty)
    prop.save()
    return prop


class PropertyFiltersLikeDislikeViewFieldsTests(TestCase):
    """ 
    Test Module for Post request form data for property filters, like & dislike view by logged 
    in student user
    """

    def setUp(self):
        self.student = createStudentUser()
        self.client = client
        self.client.force_login(user=self.student)

    def test_get_list_property_all(self):
        """Test whether all property is returened or not"""
        prop = sampleProperty(landName="LandlordUser")
        prop1 = sampleProperty(landName="LandlordUser")
        prop2 = sampleProperty(landName="LandlordUser1")
        prop3 = sampleProperty(landName="LandlordUser2")
        prop4 = sampleProperty(landName="LandlordUser3")

        response = self.client.get(reverse('property:propertyList'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 5)
    
    def test_filters_property_list(self):
        """Test all filters on the property list page"""
        am1 = amenity()
        am2 = amenity(name="Gym")
        prop1 = samplePropertyList(landName="LandlordUser", room=2, occp=10, bath=5, sqft=20000, rent=5000, amenty=[am1, am2])
        prop2 = samplePropertyList(landName="LandlordUser", room=2, occp=10, bath=5, sqft=10000, rent=30000, amenty=[am1, am2])
        prop3 = samplePropertyList(landName="LandlordUser", room=10, occp=3, bath=2, sqft=500, rent=2000, amenty=[am1, am2])
        prop4 = samplePropertyList(landName="LandlordUser", room=5, occp=10, bath=15, sqft=5000, rent=20000, amenty=[am1, am2])

        response = self.client.get(
            reverse('property:propertyList'),
            data={
                'room': ['2'], 'occp': '4', 'bath': '4', 
                'minPri': 5000, 'maxPri': 30000, 'amenities': [am1.pk, am2.pk],
                'sort': 'p_hi_low'
            }
        )
        print(response.context.get('filterSortForm').errors)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 2)
        self.assertEqual(response.context.get('object_list')[0], prop2)
        self.assertEqual(response.context.get('object_list')[1], prop1)

    def test_nolike_nodislike_view(self):
        """Test to put like on a property where no like no dislike is done"""
        prop = sampleProperty(landName="LandlordUser")
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'like': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 1)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount + 1)
        self.assertEqual(data['dislikecount'], beforedislikeCount)
    
    def test_nolike_nodislike_to_dislike_view(self):
        """Test to put dislike on a property where no like no dislike is done"""
        prop = sampleProperty(landName="LandlordUser")
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'dislike': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 1)
        self.assertEqual(data['likecount'], beforelikeCount)
        self.assertEqual(data['dislikecount'], beforedislikeCount + 1)

    def test_like_nodislike_to_remove_like_view(self):
        """Test to remove like on a property where liked, no dislike is done"""
        prop = sampleProperty(landName="LandlordUser")
        prop.likes.add(models.UserStudent.objects.get(user__user=self.student))
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'like': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount - 1)
        self.assertEqual(data['dislikecount'], beforedislikeCount)

    def test_like_nodislike_to_remove_dislike_view(self):
        """Test to remove dislike on a property where no like, disliked is done"""
        prop = sampleProperty(landName="LandlordUser")
        prop.dislikes.add(models.UserStudent.objects.get(user__user=self.student))
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'dislike': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount)
        self.assertEqual(data['dislikecount'], beforedislikeCount - 1)

    def test_liked_nodislike_to_dislike_view(self):
        """Test to dislike on a property where liked, no dislike is done"""
        prop = sampleProperty(landName="LandlordUser")
        prop.likes.add(models.UserStudent.objects.get(user__user=self.student))
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'dislike': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 1)
        self.assertEqual(data['likecount'], beforelikeCount - 1)
        self.assertEqual(data['dislikecount'], beforedislikeCount + 1)

    def test_nolike_disliked_to_like_view(self):
        """Test to like on a property where no like, disliked is done"""
        prop = sampleProperty(landName="LandlordUser")
        prop.dislikes.add(models.UserStudent.objects.get(user__user=self.student))
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'like': 1}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 1)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount + 1)
        self.assertEqual(data['dislikecount'], beforedislikeCount - 1)

    def test_like_dislike_invalid_input_view(self):
        """Test to like dislike view with invalid input"""
        prop = sampleProperty(landName="LandlordUser")
        beforelikeCount = prop.totalLikes()
        beforedislikeCount = prop.totalDislikes()
        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'like': 123}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount)
        self.assertEqual(data['dislikecount'], beforedislikeCount)

        response = self.client.post(reverse('property:propertyReaction', kwargs={'slug': prop.urlSlug}),
                        data={'dislike': 433}
                    )
        data = response.json()
        self.assertEqual(data['liked'], 0)
        self.assertEqual(data['disliked'], 0)
        self.assertEqual(data['likecount'], beforelikeCount)
        self.assertEqual(data['dislikecount'], beforedislikeCount)