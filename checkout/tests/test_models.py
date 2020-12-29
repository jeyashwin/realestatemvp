from django.test import TestCase

from checkout.models import *
from property.tests.test_models import sampleProperty
from users.tests.test_views import createStudentUser


# class CheckoutModelsTestcases(TestCase):
#     """ This class contains Testcases for all models in the Checkout App"""

#     def test_request_to_rent_property_str_representation(self):
#         """Test case to test the string representation of RequestToRentProperty model"""

#         prop = sampleProperty()
#         student = createStudentUser()
#         rentProp = RequestToRentProperty.objects.create(propertyObj=prop, studentObj=student.usertype.userstudent,
#                     occupants=2, moveIn='20-11-2019', moveOut='22-11-2020')
                
#         self.assertEqual(str(rentProp), str(rentProp.pk))