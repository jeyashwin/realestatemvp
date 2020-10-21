from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus
from PIL import Image
import tempfile, os

from users.models import UserType, UserStudent, UserLandLord, Interest

client = Client()


def MockImage(ftype='.png'):
    with tempfile.NamedTemporaryFile(suffix=ftype, delete=False) as f:
        imageFile = Image.new('RGB', (200,200), 'white')
        imageFile.save(f, 'PNG')
    return open(f.name, mode='rb')

def deleteImage(file):
    if os.path.isfile(file.path):
        os.remove(file.path)

def createInterest(name="Developer"):
    return Interest.objects.create(interest=name)

def createLandlordUser(username="TestUser"):
    data = { 'first_name': 'Test1', 'last_name': 'Test2' , 
                'email': 'TESTtest@123.com' , 'username': username,
                'password1': 'first@123', 'password2': 'first@123',
                'phone': "+12125552368", 'lanprofilePicture': MockImage()
            }
    response = client.post(
            reverse('user:landlordSignup'),
            data
    )
    landlord = get_user_model().objects.get(username=username)
    deleteImage(landlord.usertype.userlandlord.profilePicture)
    return landlord

def createStudentUser(username="TestUser"):
    in1 = createInterest()
    in2 = createInterest(name="sports")
    data = { 'first_name': 'Test1', 'last_name': 'Test2' , 
                'email': 'TESTtest@123.com' , 'username': username,
                'password1': 'first@123', 'password2': 'first@123',
                'phone': "+12125552368", 'university': 'aasd asdasd', 'classYear': 2025,
                'bio': "32423432423dsas sfas", 'profilePicture': MockImage(),
                'interests': [in1.pk, in2.pk] , 'fblink': "https://www.facebook.com/", 
                'snapLink': "https://www.snapchat.com/", 'instaLink':"https://www.instagram.com/",
                'redditLink': "https://www.reddit.com/",
            }
    response = client.post(
            reverse('user:studentSignup'),
            data
    )
    student = get_user_model().objects.get(username=username)
    deleteImage(student.usertype.userstudent.profilePicture)
    return student


class LandlordSignUpViewTests(TestCase):
    """Test Module for all Landlord Sign up requests """

    def setUp(self):
        self.validPayload = { 'first_name': 'Test Seller', 'last_name': 'TestLastname', 
                'email': 'SellerTest@Prop.com' , 'username': 'seller', 
                'password1': 'Password@123' , 'password2': 'Password@123',
                'phone': "+12125552368", 'lanprofilePicture': MockImage()
            }
        self.invalidPayload1 = { 'first_name': '', 'last_name': '', 'email': '' , 
                'username': '', 'password1': '', 'password2': '', 'phone': '',
                'lanprofilePicture': ''
            }
        self.invalidPayload2 = { 'first_name': 'saasd12123', 'last_name': 'qwqew', 'email': 'notemail' , 
                'username': 'TestUser', 'password1': '12312312', 'password2': 'Test2323', 
                'phone': "231212", 'lanprofilePicture': MockImage('.mp4')
            }

    def test_create_seller_link_without_payload(self):
        """Test creating a new Seller link user without payload"""
        response = client.get(
            reverse('user:landlordSignup')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

    def test_create_seller_valid_payload(self):
        """Test creating a new Seller user with valid payload"""
        response = client.post(
            reverse('user:landlordSignup'),
            self.validPayload
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

        user = UserType.objects.get(user__username=self.validPayload.get('username'))
        userSeller = UserLandLord.objects.get(user=user)

        self.assertEqual(user.user.email, self.validPayload.get('email').lower())
        self.assertEqual(user.user.first_name, self.validPayload.get('first_name'))
        self.assertEqual(user.user.last_name, self.validPayload.get('last_name'))
        self.assertTrue(user.user.check_password(self.validPayload.get('password1')))
        self.assertEqual(user.userType, "seller")
        self.assertFalse(user.student)
        self.assertTrue(user.landLord)
        self.assertFalse(user.is_student)
        self.assertTrue(user.is_landlord)
        self.assertEqual(userSeller.user, user)
        self.assertEqual(userSeller.phone, self.validPayload.get('phone'))
        self.assertFalse(userSeller.emailVerified)
        self.assertFalse(userSeller.phoneVerified)
        deleteImage(userSeller.profilePicture)

    def test_create_seller_invalid_payload1(self):
        """Test creating a new Seller user with invalid payload1"""
        response = client.post(
            reverse('user:landlordSignup'),
            self.invalidPayload1
        )

        errorData = response.json()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(errorData.get('first_name'), ['This field is required.'])
        self.assertEqual(errorData.get('last_name'), ['This field is required.'])
        self.assertEqual(errorData.get('email'), ['This field is required.'])
        self.assertEqual(errorData.get('username'), ['This field is required.'])
        self.assertEqual(errorData.get('password1'), ['This field is required.'])
        self.assertEqual(errorData.get('password2'), ['This field is required.'])
        self.assertEqual(errorData.get('phone'), ['This field is required.'])
        self.assertEqual(errorData.get('lanprofilePicture'), ['This field is required.'])

    def test_create_seller_invalid_payload2(self):
        """Test creating a new Seller user with invalid payload2"""
        firstUser = createLandlordUser()
        response = client.post(
            reverse('user:landlordSignup'),
            self.invalidPayload2
        )

        errorData = response.json()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(errorData.get('email'), ['Enter a valid email address.'])
        self.assertEqual(errorData.get('username'), ['A user with that username already exists.'])
        self.assertEqual(errorData.get('password2'), ["The two password fields didn't match."])
        self.assertEqual(errorData.get('phone'), ['Enter a valid phone number (e.g. +12125552368).'])
        self.assertEqual(errorData.get('lanprofilePicture'), ["File extension 'mp4' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])


class StudentSignUpViewTests(TestCase):
    """Test Module for all Landlord Sign up requests """

    def setUp(self):
        in1 = createInterest()
        in2 = createInterest("Adventure")
        self.validPayload = { 'first_name': 'Test Seller', 'last_name': 'TestLastname', 
                'email': 'SellerTEST@Prop.com' , 'username': 'student', 
                'password1': 'Password@123' , 'password2': 'Password@123',
                'phone': "+12125552368", 'university': 'aasd asdasd', 'classYear': 2025,
                'bio': "32423432423dsas sfas", 'profilePicture': MockImage(),
                'interests': [in1.pk, in2.pk], 
                'fblink': "https://www.facebook.com/", 'snapLink': "https://www.snapchat.com/", 
                'instaLink':"https://www.instagram.com/", 'redditLink': "https://www.reddit.com/",
            }
        self.invalidPayload1 = { 'first_name': '', 'last_name': '', 'email': '' , 
                'username': '', 'password1': '', 'password2': '', 'phone': '',
                'university': '', 'classYear': '' , 'bio': '', 'profilePicture': '', 'interests': [], 
                'fblink': '', 'snapLink': '', 'instaLink':'', 'redditLink': '',
            }
        self.invalidPayload2 = { 'first_name': 'saasd12123', 'last_name': 'qwqew', 'email': 'notemail' , 
                'username': 'TestUser', 'password1': '12312312', 'password2': 'Test2323', 
                'phone': "231212", 'university': 'aasd asdasd', 'classYear': 2001,
                'bio': "32423432423dsas sfas", 'profilePicture': MockImage('.avi'),
                'interests': ['123'], 'fblink': "facebook", 
                'snapLink': "snapchat", 'instaLink':"instagram",
                'redditLink': "reddit",
            }

    def test_create_student_link_without_payload(self):
        """Test creating a new Student link user without payload"""
        response = client.get(
            reverse('user:studentSignup')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

    def test_create_student_valid_payload(self):
        """Test creating a new Student user with valid payload"""
        response = client.post(
            reverse('user:studentSignup'),
            self.validPayload
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

        user = UserType.objects.get(user__username=self.validPayload.get('username'))
        userStudent = UserStudent.objects.get(user=user)

        self.assertEqual(user.user.email, self.validPayload.get('email').lower())
        self.assertEqual(user.user.first_name, self.validPayload.get('first_name'))
        self.assertEqual(user.user.last_name, self.validPayload.get('last_name'))
        self.assertTrue(user.user.check_password(self.validPayload.get('password1')))
        self.assertEqual(user.userType, "student")
        self.assertTrue(user.student)
        self.assertFalse(user.landLord)
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_landlord)
        self.assertEqual(userStudent.user, user)
        self.assertEqual(userStudent.phone, self.validPayload.get('phone'))
        self.assertEqual(userStudent.classYear, self.validPayload.get('classYear'))
        self.assertFalse(userStudent.emailVerified)
        self.assertFalse(userStudent.phoneVerified)
        self.assertTrue(userStudent.interests.filter(interest="Developer").exists)
        deleteImage(userStudent.profilePicture)

    def test_create_student_invalid_payload1(self):
        """Test creating a new Student user with invalid payload1"""
        response = client.post(
            reverse('user:studentSignup'),
            self.invalidPayload1
        )

        errorData = response.json()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(errorData.get('first_name'), ['This field is required.'])
        self.assertEqual(errorData.get('last_name'), ['This field is required.'])
        self.assertEqual(errorData.get('email'), ['This field is required.'])
        self.assertEqual(errorData.get('username'), ['This field is required.'])
        self.assertEqual(errorData.get('password1'), ['This field is required.'])
        self.assertEqual(errorData.get('password2'), ['This field is required.'])
        self.assertEqual(errorData.get('phone'), ['This field is required.'])
        self.assertEqual(errorData.get('university'), ['This field is required.'])
        self.assertEqual(errorData.get('classYear'), ['This field is required.'])
        self.assertEqual(errorData.get('bio'), ['This field is required.'])
        self.assertEqual(errorData.get('interests'), ['This field is required.'])
        self.assertEqual(errorData.get('profilePicture'), ['This field is required.'])

    def test_create_student_invalid_payload1(self):
        """Test creating a new Student user with invalid payload2"""
        firstUser = createStudentUser()
        response = client.post(
            reverse('user:studentSignup'),
            self.invalidPayload2
        )

        errorData = response.json()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        
        self.assertEqual(errorData.get('email'), ['Enter a valid email address.'])
        self.assertEqual(errorData.get('username'), ['A user with that username already exists.'])
        self.assertEqual(errorData.get('password2'), ["The two password fields didn't match."])
        self.assertEqual(errorData.get('phone'), ['Enter a valid phone number (e.g. +12125552368).'])
        self.assertEqual(errorData.get('fblink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('snapLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('instaLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('redditLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('classYear'), ['Minimum year 2010'])
        self.assertEqual(errorData.get('interests'), ['Select a valid choice. 123 is not one of the available choices.'])
        self.assertEqual(errorData.get('profilePicture'), ["File extension 'avi' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])
        self.invalidPayload2["classYear"] = 2040
        response = client.post(
            reverse('user:studentSignup'),
            self.invalidPayload2
        )
        errorData = response.json()
        self.assertEqual(errorData.get('classYear'), ['Maximum year 2030'])      


class CustomLoginViewTests(TestCase):
    """Test Module for all Login requests """

    def setUp(self):
        self.validPayloadstudent = {'username': 'TestUser', 'password': 'first@123'}
        self.validPayloadseller = {'username': 'TestUser', 'password': 'first@123'}
        self.validPayloadOtherUser = {'username': 'testOther', 'password': 'TestUserOther'}
        self.invalidPayload1 = {'username': '', 'password': ''}
        self.invalidPayload2 = {'username': 'wrong', 'password': 'first@123'}
        self.invalidPayload3 = {'username': 'TestUser', 'password': 'wrong'}

    def test_login_student_valid_payload(self):
        """Test login as valid student user"""
        user = createStudentUser()
        response = client.post(
            reverse('user:home'),
            self.validPayloadstudent
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/property/")
    
    def test_login_seller_valid_payload(self):
        """Test login as valid seller user"""
        user = createLandlordUser()
        response = client.post(
            reverse('user:home'),
            self.validPayloadseller
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/myproperty/")

    def test_login_other_user_valid_payload(self):
        """Test login as valid other user"""
        user = get_user_model().objects.create_user(username='testOther', password='TestUserOther')
        response = client.post(
            reverse('user:home'),
            self.validPayloadOtherUser
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

    def test_login_invalid_payload_1(self):
        """Test login with invalid inputs payload1"""
        response = client.post(
            reverse('user:home'),
            self.invalidPayload1
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('form').errors["username"],  ['This field is required.'])
        self.assertEqual(response.context.get('form').errors["password"],  ['This field is required.'])

    def test_login_invalid_payload_2(self):
        """Test login with invalid inputs payload2 with wrong username"""
        user = createLandlordUser()
        response = client.post(
            reverse('user:home'),
            self.invalidPayload2
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('form').errors['__all__'],  ['Please enter a correct username and password. Note that both fields may be case-sensitive.'])

    def test_login_invalid_payload_3(self):
        """Test login with invalid inputs payload2 with wrong password"""
        user = createLandlordUser()
        response = client.post(
            reverse('user:home'),
            self.invalidPayload3
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context.get('form').errors['__all__'],  ['Please enter a correct username and password. Note that both fields may be case-sensitive.'])


class StudentProfileUpdateViewTests(TestCase):
    """Test Update View request that require authentication of students"""

    def setUp(self):
        int1 = createInterest("Sports")
        self.student = createStudentUser()
        self.client = client
        self.client.force_login(user=self.student)
        self.validPayload = {'first_name': 'Testfirst', 'last_name': 'Testlast' , 
                'email': 'TESTEmail@123.com' , 'phone': "+12345678901", 'university': 'Test college', 
                'classYear': 2015, 'bio': "test bio data", 'profilePicture': MockImage('.jpg'),
                'interests': [int1.pk] , 'fbLink': "https://www.facebook.com/", 
                'snapLink': "https://www.snapchat.com/", 'instaLink':"https://www.instagram.com/",
                'redditLink': "https://www.reddit.com/",
            }
        self.invalidPayload1 = {'first_name': '', 'last_name': '' , 'email': '' , 'phone': "", 
                'university': '', 'classYear': '', 'bio': "", 'profilePicture': '', 'interests': [] 
                , 'fbLink': "", 'snapLink': "", 'instaLink':"", 'redditLink': "",
            }
        self.invalidPayload2 = {'email': 'TESTEmail' , 'phone': "+1234567", 'classYear': 2040, 
                'profilePicture': MockImage('.mp4'), 'interests': [10] , 'fbLink': "facebook", 
                'snapLink': "zsfsdf", 'instaLink':"dfsdf", 'redditLink': "adas",}

    def test_retrieve_student_profile_success(self):
        """Test retrieving profile for logged in student user"""
        response = self.client.get(
                reverse('user:studentProfile', kwargs={'username': self.student.username})
            )
        resObject = response.context.get("object")
        studentObject = UserStudent.objects.get(user__user=self.student)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(resObject.user.user, response.context.get('user'))
        self.assertEqual(resObject.user.user.first_name, self.student.first_name)
        self.assertEqual(resObject.user.user.last_name, self.student.last_name)
        self.assertEqual(resObject.user.user.email, self.student.email)
        self.assertEqual(resObject.phone, studentObject.phone)
        self.assertEqual(resObject.profilePicture, studentObject.profilePicture)
        self.assertEqual(resObject.interests, studentObject.interests)

    def test_retrieve_student_profile_failed(self):
        """Test retrieving profile for not logged in student user using logged in user"""
        otherUser = createStudentUser(username="Test")
        response = self.client.get(
                reverse('user:studentProfile', kwargs={'username': otherUser.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_update_student_profile_failed(self):
        """Test updating profile for not logged in student user using logged in user"""
        otherUser = createStudentUser(username="Test")
        response = self.client.post(
                reverse('user:studentProfile', kwargs={'username': otherUser.username}),
                data=self.validPayload
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_update_student_profile_with_validPayload(self):
        """Test updating profile for logged in student user"""
        studentObject = UserStudent.objects.get(user__user=self.student)
        profilePicBeforeUp = studentObject.profilePicture
        response = self.client.post(
                reverse('user:studentProfile', kwargs={'username': self.student.username}),
                data=self.validPayload
            )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/student/profile/{}/'.format(self.student.username))

        studentObject.refresh_from_db()

        self.assertEqual(studentObject.user.user.first_name, self.validPayload.get('first_name'))
        self.assertEqual(studentObject.user.user.last_name, self.validPayload.get('last_name'))
        self.assertEqual(studentObject.user.user.email, self.validPayload.get('email').lower())
        self.assertEqual(studentObject.phone, self.validPayload.get('phone'))
        self.assertEqual(studentObject.university, self.validPayload.get('university'))
        self.assertEqual(studentObject.classYear, self.validPayload.get('classYear'))
        self.assertEqual(studentObject.profilePicture.url[-4:], ".jpg")
        self.assertTrue(os.path.isfile(studentObject.profilePicture.path))
        self.assertEqual(studentObject.bio, self.validPayload.get('bio'))
        self.assertTrue(studentObject.interests.filter(pk__in=self.validPayload.get('interests')).exists())
        self.assertEqual(studentObject.fbLink, self.validPayload.get('fbLink'))

        deleteImage(studentObject.profilePicture)

    def test_update_student_profile_with_invalidPayload1(self):
        """Test updating profile for logged in student user with invalid payload1"""
        studentObject = UserStudent.objects.get(user__user=self.student)
        response = self.client.post(
                reverse('user:studentProfile', kwargs={'username': self.student.username}),
                data=self.invalidPayload1
            )
        errorData = response.context.get('form').errors
        self.assertEqual(response.status_code, HTTPStatus.OK)

        studentObject.refresh_from_db()
        self.assertNotEqual(studentObject.user.user.first_name, self.invalidPayload1.get('first_name'))
        self.assertNotEqual(studentObject.phone, self.invalidPayload1.get('phone'))
        self.assertEqual(errorData["first_name"],  ['This field is required.'])
        self.assertEqual(errorData["last_name"],  ['This field is required.'])
        self.assertEqual(errorData["email"],  ['This field is required.'])
        self.assertEqual(errorData["phone"],  ['This field is required.'])
        self.assertEqual(errorData["university"],  ['This field is required.'])
        self.assertEqual(errorData["classYear"],  ['This field is required.'])
        self.assertEqual(errorData["bio"],  ['This field is required.'])
        self.assertEqual(errorData["interests"],  ['This field is required.'])
        self.assertEqual(errorData.get("fbLink", None), None)

    def test_update_student_profile_with_invalidPayload2(self):
        """Test updating profile for logged in student user with invalid payload2"""
        studentObject = UserStudent.objects.get(user__user=self.student)
        response = self.client.post(
                reverse('user:studentProfile', kwargs={'username': self.student.username}),
                data=self.invalidPayload2
            )
        errorData = response.context.get('form').errors
        self.assertEqual(response.status_code, HTTPStatus.OK)

        studentObject.refresh_from_db()
        self.assertNotEqual(studentObject.user.user.email, self.invalidPayload2.get('email'))
        self.assertNotEqual(studentObject.phone, self.invalidPayload2.get('phone'))
        self.assertEqual(errorData["email"],  ['Enter a valid email address.'])
        self.assertEqual(errorData["phone"],  ['Enter a valid phone number (e.g. (201) 555-0123) or a number with an international call prefix.'])
        self.assertEqual(errorData["classYear"],  ['Maximum year 2030'])
        self.assertEqual(errorData['profilePicture'], ["File extension 'mp4' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])
        self.assertEqual(errorData["interests"],  ['Select a valid choice. 10 is not one of the available choices.'])
        self.assertEqual(errorData.get('fbLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('snapLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('instaLink'), ['Enter a valid URL.'])
        self.assertEqual(errorData.get('redditLink'), ['Enter a valid URL.'])


class LandlordProfileUpdateViewTests(TestCase):
    """Test Update View request that require authentication of landlord"""

    def setUp(self):
        self.landlord = createLandlordUser()
        self.client = client
        self.client.force_login(user=self.landlord)
        self.validPayload = {'first_name': 'Testfirst', 'last_name': 'Testlast' , 
                'email': 'TESTEmail@123.com' , 'phone': "+12345678901",
                'profilePicture': MockImage('.jpg'),
            }
        self.invalidPayload1 = {'first_name': '', 'last_name': '' , 'email': '' , 'phone': "", 
                'profilePicture': '' }
        self.invalidPayload2 = {'email': 'TESTEmail' , 'phone': "+1234567", 
                'profilePicture': MockImage('.mp4') }

    def test_retrieve_landlord_profile_success(self):
        """Test retrieving profile for logged in landlord user"""
        response = self.client.get(
                reverse('user:landlordProfile', kwargs={'username': self.landlord.username})
            )
        resObject = response.context.get("object")
        landlordObject = UserLandLord.objects.get(user__user=self.landlord)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(resObject.user.user, response.context.get('user'))
        self.assertEqual(resObject.user.user.first_name, self.landlord.first_name)
        self.assertEqual(resObject.user.user.last_name, self.landlord.last_name)
        self.assertEqual(resObject.user.user.email, self.landlord.email)
        self.assertEqual(resObject.phone, landlordObject.phone)
        self.assertEqual(resObject.profilePicture, landlordObject.profilePicture)

    def test_retrieve_landlord_profile_failed(self):
        """Test retrieving profile for not logged in landlord user using logged in user"""
        otherUser = createLandlordUser(username="Test")
        response = self.client.get(
                reverse('user:landlordProfile', kwargs={'username': otherUser.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_update_landlord_profile_failed(self):
        """Test updating profile for not logged in landlord user using logged in user"""
        otherUser = createLandlordUser(username="Test")
        response = self.client.post(
                reverse('user:landlordProfile', kwargs={'username': otherUser.username}),
                data=self.validPayload
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_update_landlord_profile_with_validPayload(self):
        """Test updating profile for logged in landlord user"""
        landlordObject = UserLandLord.objects.get(user__user=self.landlord)
        profilePicBeforeUp = landlordObject.profilePicture
        response = self.client.post(
                reverse('user:landlordProfile', kwargs={'username': self.landlord.username}),
                data=self.validPayload
            )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/landlord/profile/{}/'.format(self.landlord.username))

        landlordObject.refresh_from_db()

        self.assertEqual(landlordObject.user.user.first_name, self.validPayload.get('first_name'))
        self.assertEqual(landlordObject.user.user.last_name, self.validPayload.get('last_name'))
        self.assertEqual(landlordObject.user.user.email, self.validPayload.get('email').lower())
        self.assertEqual(landlordObject.phone, self.validPayload.get('phone'))
        self.assertEqual(landlordObject.profilePicture.url[-4:], ".jpg")
        self.assertTrue(os.path.isfile(landlordObject.profilePicture.path))

        deleteImage(landlordObject.profilePicture)

    def test_update_landlord_profile_with_invalidPayload1(self):
        """Test updating profile for logged in landlord user with invalid payload1"""
        landlordObject = UserLandLord.objects.get(user__user=self.landlord)
        response = self.client.post(
                reverse('user:landlordProfile', kwargs={'username': self.landlord.username}),
                data=self.invalidPayload1
            )
        errorData = response.context.get('form').errors
        self.assertEqual(response.status_code, HTTPStatus.OK)

        landlordObject.refresh_from_db()
        self.assertNotEqual(landlordObject.user.user.first_name, self.invalidPayload1.get('first_name'))
        self.assertNotEqual(landlordObject.phone, self.invalidPayload1.get('phone'))
        self.assertEqual(errorData["first_name"],  ['This field is required.'])
        self.assertEqual(errorData["last_name"],  ['This field is required.'])
        self.assertEqual(errorData["email"],  ['This field is required.'])
        self.assertEqual(errorData["phone"],  ['This field is required.'])

    def test_update_landlord_profile_with_invalidPayload2(self):
        """Test updating profile for logged in landlord user with invalid payload2"""
        landlordObject = UserLandLord.objects.get(user__user=self.landlord)
        response = self.client.post(
                reverse('user:landlordProfile', kwargs={'username': self.landlord.username}),
                data=self.invalidPayload2
            )
        errorData = response.context.get('form').errors
        self.assertEqual(response.status_code, HTTPStatus.OK)

        landlordObject.refresh_from_db()
        self.assertNotEqual(landlordObject.user.user.first_name, self.validPayload.get('first_name'))
        self.assertNotEqual(landlordObject.user.user.last_name, self.validPayload.get('last_name'))
        self.assertEqual(errorData["email"],  ['Enter a valid email address.'])
        self.assertEqual(errorData["phone"],  ['Enter a valid phone number (e.g. (201) 555-0123) or a number with an international call prefix.'])
        self.assertEqual(errorData['profilePicture'], ["File extension 'mp4' is not allowed. Allowed extensions are: 'bmp, dib, gif, tif, tiff, jfif, jpe, jpg, jpeg, pbm, pgm, ppm, pnm, png, apng, blp, bufr, cur, pcx, dcx, dds, ps, eps, fit, fits, fli, flc, ftc, ftu, gbr, grib, h5, hdf, jp2, j2k, jpc, jpf, jpx, j2c, icns, ico, im, iim, mpg, mpeg, mpo, msp, palm, pcd, pdf, pxr, psd, bw, rgb, rgba, sgi, ras, tga, icb, vda, vst, webp, wmf, emf, xbm, xpm'."])


class UserDeleteViewTests(TestCase):
    """Test Delete View request that require authentication of User"""

    def setUp(self):
        self.landlord = createLandlordUser()
        self.student = createStudentUser(username="student")
        self.client = client

    def test_landlord_delete_success(self):
        """Test deletion of landlord profile for logged in landlord user"""
        self.client.force_login(user=self.landlord)
        response = self.client.get(
                reverse('user:deleteProfile', kwargs={'username': self.landlord.username})
            )
        resObject = response.context.get("object")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(resObject, response.context.get('user'))
        response = self.client.post(
                reverse('user:deleteProfile', kwargs={'username': self.landlord.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        self.assertFalse(UserLandLord.objects.filter(user__user=self.landlord).exists())

        response = self.client.get(reverse('user:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context.get('user').is_authenticated)

    def test_landlord_delete_failed(self):
        """Test deletion of landlord profile for not logged in landlord user by logged in landlord"""
        self.client.force_login(user=self.landlord)
        otherLandlord = createLandlordUser(username="Test")
        response = self.client.get(
                reverse('user:deleteProfile', kwargs={'username': otherLandlord.username})
            )        
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(
                reverse('user:deleteProfile', kwargs={'username': otherLandlord.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
 
    def test_student_delete_success(self):
        """Test deletion of student profile for logged in student user"""
        self.client.force_login(user=self.student)
        response = self.client.get(
                reverse('user:deleteProfile', kwargs={'username': self.student.username})
            )
        resObject = response.context.get("object")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(resObject, response.context.get('user'))

        response = self.client.post(
                reverse('user:deleteProfile', kwargs={'username': self.student.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/')
        self.assertFalse(UserStudent.objects.filter(user__user=self.student).exists())

        response = self.client.get(reverse('user:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context.get('user').is_authenticated)

    def test_student_delete_failed(self):
        """Test deletion of student profile for not logged in student user by logged in student"""
        self.client.force_login(user=self.student)
        otherStudent = createStudentUser(username="Test")
        response = self.client.get(
                reverse('user:deleteProfile', kwargs={'username': otherStudent.username})
            )        
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.post(
                reverse('user:deleteProfile', kwargs={'username': otherStudent.username})
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class PrivateAccessTests(TestCase):
    """Test View request that require authentication"""

    def test_student_profile_view(self):
        """Test get & post request login required for student profile view"""

        response = client.get(reverse('user:studentProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/student/profile/TestUser/')

        response = client.post(reverse('user:studentProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/student/profile/TestUser/')

    def test_landlord_profile_view(self):
        """Test get & post request login required for landlord profile view"""

        response = client.get(reverse('user:landlordProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/landlord/profile/TestUser/')

        response = client.post(reverse('user:landlordProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/landlord/profile/TestUser/')

    def test_user_delete_view(self):
        """Test get & post request login required for user delete view"""

        response = client.get(reverse('user:deleteProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/delete/profile/TestUser/')

        response = client.post(reverse('user:deleteProfile', kwargs={'username': "TestUser"}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, '/?next=/delete/profile/TestUser/')