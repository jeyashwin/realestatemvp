from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

from services.models import Service
from services.views import ServiceListView, ServiceDetailView
from users.models import UserType, UserLandLord, UserStudent

client = Client()

def sampleService(name='Bed'):
    return Service.objects.create(serviceName=name, description="Nice branded and comfort bed",
                    rentCycle='monthly', price=2000)


class PrivateAccessServiceTests(TestCase):
    """Test service View request that require authentication"""

    def test_service_list_view_get_post_without_login(self):
        """Test that list view is accessed without login"""
        service = sampleService()
        response = client.get(reverse('services:servicesList'))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/services/')

        response = client.post(reverse('services:servicesList'))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/services/')

    def test_service_detail_view_get_post_without_login(self):
        """Test that detail view is accessed without login"""
        service = sampleService()
        response = client.get(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f'/?next=/services/{service.pk}')

        response = client.post(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f'/?next=/services/{service.pk}')


class PrivateLandlordAccessServiceTests(TestCase):
    """Test service View request that require authentication but not as landlord"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testlandserviceview', 
                    password="seller@123")
        usertype = UserType.objects.create(user=self.user, userType='seller')
        landlord = UserLandLord.objects.create(user=usertype, phone="+12345678901", 
                    profilePicture="1.jpg",
                )
        self.client = client
        self.client.force_login(user=self.user)

    def test_service_list_view_get_post_request_as_landlord(self):
        """Test that list view is accessed using landlord account"""
        service = sampleService()
        response = client.get(reverse('services:servicesList'))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = client.post(reverse('services:servicesList'))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_service_detail_view_get_post_request_as_landlord(self):
        """Test that detail view is accessed using landlord account"""
        service = sampleService()
        response = client.get(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        response = client.post(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class PrivateStudentAccessServiceTests(TestCase):
    """Test service View request that require authentication of student account"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='teststudserviceview', 
                        password="Student@123")
        usertype = UserType.objects.create(user=self.user, userType='student')
        self.student = UserStudent.objects.create(user=usertype, phone="+12345678901", 
                        university='Test college', classYear=2015, bio="test bio data", 
                        profilePicture="1.jpg",
                    )
        self.client = client
        self.client.force_login(user=self.user)

    def test_service_list_view_get_post_request_as_student(self):
        """Test that service list view can be accessed using student account"""
        service = sampleService()
        service1 = sampleService(name='car')
        service2 = sampleService(name='TV')
        service3 = sampleService(name='Fridge')
        service4 = sampleService(name='Washing Machine')
        service5 = sampleService(name='Grass cuttor')
        service6 = sampleService(name='Water pump')
        service7 = sampleService(name='Dish washer')
        service8 = sampleService(name='Sofa')
        service9 = sampleService(name='Cooker')
        service10 = sampleService(name='bike')
        response = client.get(reverse('services:servicesList'))

        objectlist = response.context.get('object_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 10)
        self.assertEqual(objectlist[9], service1)
        self.assertEqual(objectlist[8], service2)
        self.assertEqual(objectlist[7], service3)
        self.assertEqual(objectlist[6], service4)
        self.assertEqual(objectlist[5], service5)
        self.assertEqual(objectlist[4], service6)
        self.assertEqual(objectlist[3], service7)
        self.assertEqual(objectlist[2], service8)
        self.assertEqual(objectlist[1], service9)
        self.assertEqual(objectlist[0], service10)
        self.assertEqual(response.context.get('total_pages'), [1, 2])
        self.assertEqual(response.context.get('page_obj').number, 1)

        response = client.get(f"{reverse('services:servicesList')}?page=2")
        objectlist = response.context.get('object_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 1)
        self.assertEqual(objectlist[0], service)
        self.assertEqual(response.context.get('total_pages'), [1, 2])
        self.assertEqual(response.context.get('page_obj').number, 2)

        response = client.post(reverse('services:servicesList'))

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
    
    def test_service_list_view_search(self):
        """Test that service list view search can be accessed using student account and 
        functions correctly
        """
        service = sampleService()
        service1 = sampleService(name='bed2')
        service2 = sampleService(name='Samsung Tv')
        service3 = sampleService(name='Samsung Fridge')

        response = client.get(reverse('services:servicesList'))
        objectlist = response.context.get('object_list')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 4)

        response = client.get(f"{reverse('services:servicesList')}?serviceName=bed")
        objectlist = response.context.get('object_list')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 2)
        self.assertEqual(objectlist[1], service)
        self.assertEqual(objectlist[0], service1)

        response = client.get(f"{reverse('services:servicesList')}?serviceName=sam")
        objectlist = response.context.get('object_list')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 2)
        self.assertEqual(objectlist[1], service2)
        self.assertEqual(objectlist[0], service3)

        response = client.get(f"{reverse('services:servicesList')}?serviceName=samsung tv")
        objectlist = response.context.get('object_list')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 1)
        self.assertEqual(objectlist[0], service2)

    def test_service_list_view_search_with_pages(self):
        """Test that service list view search with pages can be accessed using student account and 
        functions correctly
        """
        service = sampleService()
        service1 = sampleService()
        service2 = sampleService()
        service3 = sampleService()
        service4 = sampleService()
        service5 = sampleService()
        service6 = sampleService()
        service7 = sampleService()
        service8 = sampleService()
        service9 = sampleService()
        service10 = sampleService()

        response = client.get(f"{reverse('services:servicesList')}?serviceName=bed")
        objectlist = response.context.get('object_list')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 10)
        self.assertEqual(response.context.get('total_pages'), [1, 2])
        self.assertEqual(response.context.get('page_obj').number, 1)

        response = client.get(f"{reverse('services:servicesList')}?serviceName=bed&page=2")
        objectlist = response.context.get('object_list')
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('object_list').count(), 1)
        self.assertEqual(response.context.get('total_pages'), [1, 2])
        self.assertEqual(response.context.get('page_obj').number, 2)
        self.assertEqual(objectlist[0], service)

    def test_service_detail_view_get_post_request_as_student(self):
        """Test that detail view is accessed using student account"""
        service = sampleService()
        response = client.get(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        obj = response.context.get('object')
        self.assertEqual(obj.serviceName, service.serviceName)
        self.assertEqual(obj.description, service.description)
        self.assertEqual(obj.rentCycle, service.rentCycle)
        self.assertEqual(obj.price, service.price)

        response = client.get(reverse('services:servicesDetail', kwargs={'pk': 123}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = client.post(reverse('services:servicesDetail', kwargs={'pk': service.pk}))

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)