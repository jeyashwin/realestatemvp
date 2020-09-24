from django.test import TestCase, Client
from django.urls import reverse

from users.models import UserType, UserStudent, UserLandLord

client = Client()


def createUser(regUserType="student"):
    data = { 'first_name': 'Test1', 'last_name': 'Test2' , 
                'email': 'TESTtest@123.com' , 'regUserType': regUserType, 'is_college_student': 'on', 
                'college_name': 'Test college' , 'date_of_birth': '2020-09-23', 
                'password1': 'first@123', 'password2': 'first@123'
            }
    response = client.post(
            reverse('user:signup'),
            data
    )
    return response


class SignUpClassViewTests(TestCase):
    """Test Module for all Sign up requests """

    def setUp(self):
        self.validPayloadStudent = { 'first_name': 'Test1', 'last_name': 'Test2' , 
                'email': 'TESTtest@123.com' , 'regUserType': 'student', 'is_college_student': 'on', 
                'college_name': 'Test college' , 'date_of_birth': '2020-09-23', 
                'password1': 'first@123', 'password2': 'first@123'
            }
        self.validPayloadSeller = { 'first_name': 'Test Seller', 'last_name': 'TestLastname', 
                'email': 'SellerTest@Prop.com' , 'regUserType': 'seller', 
                'date_of_birth': '1998-09-23' , 'password1': 'Password@123' , 
                'password2': 'Password@123'
            }
        self.invalidPayload1 = { 'first_name': '', 'last_name': '', 'email': '' , 
                'regUserType': '', 'date_of_birth': '', 'password1': '', 
                'password2': ''
            }
        self.invalidPayload2 = { 'first_name': 'saasd12123', 'last_name': 'qwqew', 'email': 'notemail' , 
                'regUserType': 'weqwasd', 'date_of_birth': '211321asd', 'password1': '12312312', 
                'password2': 'Test2323'
            }
        self.emailPayloadStudent = { 'first_name': 'Test1', 'last_name': 'Test2' , 
                'email': 'TESTtest@123.com' , 'regUserType': 'student', 'is_college_student': 'on', 
                'college_name': 'Test college' , 'date_of_birth': '2020-09-23', 
                'password1': 'first@123', 'password2': 'first@123'
            }
        self.emailPayloadSeller = { 'first_name': 'Test Seller', 'last_name': 'TestLastname', 
                'email': 'SellerTest@Prop.com' , 'regUserType': 'seller', 
                'date_of_birth': '1998-09-23' , 'password1': 'Password@123' , 
                'password2': 'Password@123'
            }
        
    def test_create_student_valid_payload(self):
        """Test creating a new student user with valid payload"""
        response = client.post(
            reverse('user:signup'),
            self.validPayloadStudent
        )

        self.assertEqual(response.status_code, 201)

        user = UserType.objects.get(user__email="testtest@123.com")
        userStudent = UserStudent.objects.get(user=user)
        
        self.assertEqual(user.user.email, "testtest@123.com")
        self.assertEqual(user.user.username, "Test1")
        self.assertTrue(user.user.check_password(self.validPayloadStudent['password1']))
        self.assertEqual(user.userType, self.validPayloadStudent['regUserType'])
        self.assertEqual(user.student, True)
        self.assertEqual(user.landLord, False)
        self.assertEqual(user.is_student, True)
        self.assertEqual(user.is_landlord, False)
        self.assertEqual(userStudent.isCollegeStudent, True)
        self.assertEqual(userStudent.collegeName, "Test college")

    def test_create_seller_valid_payload(self):
        """Test creating a new Seller user with valid payload"""
        response = client.post(
            reverse('user:signup'),
            self.validPayloadSeller
        )
        self.assertEqual(response.status_code, 201)

        user = UserType.objects.get(user__email="sellertest@prop.com")
        userSeller = UserLandLord.objects.get(user=user)
        
        self.assertEqual(user.user.email, "sellertest@prop.com")
        self.assertEqual(user.user.username, "TestSeller")
        self.assertTrue(user.user.check_password(self.validPayloadSeller['password1']))
        self.assertEqual(user.userType, self.validPayloadSeller['regUserType'])
        self.assertEqual(user.student, False)
        self.assertEqual(user.landLord, True)
        self.assertEqual(user.is_student, False)
        self.assertEqual(user.is_landlord, True)
        self.assertEqual(userSeller.user, user)
    
    def test_create_user_valid_payload(self):
        """Test creating a new Seller user with valid payload"""
        userStudent = createUser()
        userSeller = createUser(regUserType="seller")
        
        self.assertEqual(userStudent.status_code, 201)
        self.assertEqual(userSeller.status_code, 201)

    def test_create_user_invalid_payload_one(self):
        """Test creating a new user with invalid payload 1"""
        response = client.post(
            reverse('user:signup'),
            self.invalidPayload1
        )
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("first_name"), ['This field is required.'])
        self.assertEqual(data.get("last_name"), ['This field is required.'])
        self.assertEqual(data.get("email"), ['This field is required.'])
        self.assertEqual(data.get("regUserType"), ['This field is required.'])
        self.assertEqual(data.get("date_of_birth"), ['This field is required.'])
        self.assertEqual(data.get("password1"), ['This field is required.'])
        self.assertEqual(data.get("password2"), ['This field is required.'])
    
    def test_create_user_invalid_payload_two(self):
        """Test creating a new user with invalid payload 2"""
        response = client.post(
            reverse('user:signup'),
            self.invalidPayload2
        )
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("email"), ['Enter a valid email address.'])
        self.assertEqual(data.get("regUserType"), [
            ('Select a valid choice. {} is not one of the available choices.').format(self.invalidPayload2.get('regUserType'))
        ])
        self.assertEqual(data.get("date_of_birth"), ['Enter a valid date.'])
        self.assertEqual(data.get("password2"), ["The two password fields didn't match."])

    def test_create_student_with_existing_email(self):
        """Test creating a new student with existing email"""
        response1 = client.post(
            reverse('user:signup'),
            self.validPayloadStudent
        )
        self.assertEqual(response1.status_code, 201)
        response2 = client.post(
            reverse('user:signup'),
            self.emailPayloadStudent
        )
        data = response2.json()
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(data.get("email"), ['Email already exists!'])

    def test_create_seller_with_existing_email(self):
        """Test creating a new seller with existing email"""
        response1 = client.post(
            reverse('user:signup'),
            self.validPayloadSeller
        )
        self.assertEqual(response1.status_code, 201)
        response2 = client.post(
            reverse('user:signup'),
            self.validPayloadSeller
        )
        data = response2.json()
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(data.get("email"), ['Email already exists!'])


class UserLoginClassViewTests(TestCase):
    """Test Module for all Login requests """

    def setUp(self):
        self.validPayloadstudent = {'login_email': 'TESTtest@123.com', 'login_password': 'first@123', 
                                'logUserType': 'student'}
        self.validPayloadseller = {'login_email': 'TESTtest@123.com', 'login_password': 'first@123', 
                                'logUserType': 'seller'}
        self.invalidPayload1 = {'login_email': '', 'login_password': '', 
                                'logUserType': ''}
        self.invalidPayload2 = {'login_email': 'noemail', 'login_password': 'asdad', 
                                'logUserType': 'sdad'}
        self.invalidPass1 = {'login_email': 'TestTest@123.com', 'login_password': '@123', 
                                'logUserType': 'student'}
        self.invalidPass2 = {'login_email': 'TestTEST@123.com', 'login_password': '123123sdad@123', 
                                'logUserType': 'seller'}

    def test_login_student_valid_payload(self):
        """Test login as valid student user"""
        user = createUser()
        response = client.post(
            reverse('user:login'),
            self.validPayloadstudent
        )
        self.assertEqual(response.status_code, 302)
    
    def test_login_seller_valid_payload(self):
        """Test login as valid seller user"""
        user = createUser(regUserType="seller")
        response = client.post(
            reverse('user:login'),
            self.validPayloadseller
        )
        self.assertEqual(response.status_code, 302)
    
    def test_login_invalid_payload_one(self):
        """Test login as invalid inputs payload1"""
        response = client.post(
            reverse('user:login'),
            self.invalidPayload1
        )
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("login_email"), ['This field is required.'])
        self.assertEqual(data.get("login_password"), ['This field is required.'])
        self.assertEqual(data.get("logUserType"), ['This field is required.'])

    def test_login_invalid_payload_two(self):
        """Test login as invalid inputs payload2"""
        response = client.post(
            reverse('user:login'),
            self.invalidPayload2
        )
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("login_email"), ['Enter a valid email address.'])
        self.assertEqual(data.get("logUserType"), [
            ('Select a valid choice. {} is not one of the available choices.').format(self.invalidPayload2.get('logUserType'))
        ])

    def test_login_valid_payload_invalid_email(self):
        """Test login as valid payload but invalid email"""
        responseStudent = client.post(
            reverse('user:login'),
            self.validPayloadstudent
        )
        responseSeller = client.post(
            reverse('user:login'),
            self.validPayloadseller
        )
        self.assertEqual(responseStudent.status_code, 404)
        self.assertEqual(responseSeller.status_code, 404)

    def test_login_valid_email_invalid_pass(self):
        """Test login as valid email but invalid pass"""
        userStudent = createUser()
        userSeller = createUser(regUserType="seller")
        responseStudent = client.post(
            reverse('user:login'),
            self.invalidPass1
        )
        responseSeller = client.post(
            reverse('user:login'),
            self.invalidPass2
        )
        self.assertEqual(responseStudent.status_code, 404)
        self.assertEqual(responseSeller.status_code, 404)
