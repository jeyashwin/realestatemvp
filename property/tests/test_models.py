from django.test import TestCase
from django.forms import ValidationError

from PIL import Image
import datetime, tempfile, os

from property import models, taskSchedulers
from users.tests.test_views import createStudentUser, createLandlordUser
from users.models import UserLandLord, UserStudent

def sampleProperty(landName=None, zipcode=88030, amount=1000, fromD=datetime.date.today(), toD=datetime.date.today() + datetime.timedelta(days=2)):
    if landName is None:
        landlord = createLandlordUser()
    else:
        landlord = createLandlordUser(username=landName)
    stud1 = createStudentUser(username="Test")
    stud2 = createStudentUser(username="Test1")
    stud3 = createStudentUser(username="Test2")
    stud1Object = UserStudent.objects.get(user__user=stud1)
    stud2Object = UserStudent.objects.get(user__user=stud2)
    stud3Object = UserStudent.objects.get(user__user=stud3)
    landlordObject = UserLandLord.objects.get(user__user=landlord)
    state = models.StateList.objects.create(stateFullName="New Mexico", stateShortName="NM")
    city = models.CityList.objects.create(state=state, cityName="Deming")
    amenity1 = models.Amenities.objects.create(amenityType="Internet")
    amenity2 = models.Amenities.objects.create(amenityType="Pool")
    prop = models.Property.objects.create(landlord=landlordObject, 
            city=city, zipcode=zipcode, address="91/2 I-10,", sqft="1000", occupants=10, rooms=10,
            bathrooms=6, securityDeposit=True, amount=amount, rentPerPerson=2000, 
            description="asdas asdas", utilities=True, garage=True, parkingSpace=10, 
            fromDate=fromD, toDate=toD
        )
    prop.amenities.set([amenity1, amenity2])
    prop.likes.set([stud1Object, stud3Object])
    prop.dislikes.set([stud2Object])
    prop.save()
    try:
        prop.clean()
    except:
        pass

    jobs = taskSchedulers.scheduler.get_jobs()
    for job in jobs:
        job.remove()

    return prop


class PropertyModelTests(TestCase):
    """ Test all the  models in Property App"""

    def test_statelist_str(self):
        """Test the statelist string representation"""
        state = models.StateList.objects.create(stateFullName="Newyork", stateShortName="NY")

        self.assertEqual(str(state), state.stateFullName)

    def test_citylist_str(self):
        """Test the citylist string representation"""
        state = models.StateList.objects.create(stateFullName="Ozark", stateShortName="OZ")
        city = models.CityList.objects.create(state=state, cityName="Los Angeles")

        self.assertEqual(str(city), "{}, {}".format(city.cityName, state.stateShortName))
    
    def test_amenities_str(self):
        """Test the amenities string representation"""
        amenity = models.Amenities.objects.create(amenityType="Internet")

        self.assertEqual(str(amenity), amenity.amenityType)
    
    def test_product_model_with_valid_input(self):
        """Test the product model string representation with valid input"""
        propObject = sampleProperty()

        self.assertEqual(str(propObject), "{} {}".format(propObject.pk, propObject.title))
        self.assertEqual(propObject.urlSlug, "912-i-10-deming-nm-88030")
        self.assertEqual(propObject.totalLikes(), 2)
        self.assertEqual(propObject.totalDislikes(), 1)

    def test_product_model_with_invalid_input(self):
        """Test the product model string representation with invalid input"""
        fromDateInvalid = datetime.date(2020, 10, 5)
        toDateInvalid = datetime.date(2020, 10, 1)
        propObject = sampleProperty(amount=None, 
                        fromD=fromDateInvalid,
                        toD=toDateInvalid
                    )
        with self.assertRaises(ValidationError):
            propObject.full_clean()
        
        try:
            propObject.full_clean()
        except ValidationError as e:
            self.assertEqual(dict(e).get("amount"), ["Amount Field is required"])
            self.assertEqual(dict(e).get("toDate"), ["To Date cannot be less than or equal to From Date."])

    def test_property_image_str(self):
        """Test the product Image model string representation"""
        propObject = sampleProperty()
        propImage = models.PropertyImage.objects.create(propertyKey=propObject, 
                        imageDescription="Bedroom", imagePath="1.jpg")

        self.assertEqual(str(propImage), str(propImage.pk))
        self.assertEqual(propImage.mediaType, 'propimage')
        self.assertEqual(propImage.imagePath, '1.jpg')

    def test_property_video_str(self):
        """Test the product Video model string representation"""
        propObject = sampleProperty()
        propVideo = models.PropertyVideo.objects.create(propertyKey=propObject, 
                        videoDescription="Hall", videoPath="1.mp4")

        self.assertEqual(str(propVideo), str(propVideo.pk))
        self.assertEqual(propVideo.mediaType, 'propvideo')
        self.assertEqual(propVideo.videoPath, '1.mp4')

    def test_post_question_str(self):
        """Test the post question model string representation"""
        propObject = sampleProperty()
        stud1 = createStudentUser(username="Test")
        stud1Object = UserStudent.objects.get(user__user=stud1)
        postQuestion = models.PostQuestion.objects.create(propKey=propObject, 
                        student=stud1Object, question="Do the property have Water supply?")

        self.assertEqual(str(postQuestion), postQuestion.question)
    
    def test_post_answer_str(self):
        """Test the post Answer model string representation"""
        propObject = sampleProperty()
        stud1 = createStudentUser(username="Test")
        stud1Object = UserStudent.objects.get(user__user=stud1)
        postQuestion = models.PostQuestion.objects.create(propKey=propObject, 
                        student=stud1Object, question="Do the property have Water supply?")
        postAnswer = models.PostAnswer.objects.create(question=postQuestion, 
                        answer="We have 24 hrs water supply.")

        self.assertEqual(str(postAnswer), postAnswer.answer)

#property models new fields valid, invalid
#property address geo location check
#property title check
#property nearby model str, valid, invalid fields
#property jobstore model str, valid, invalid fields
#property presave check
#property post save check
#property fetch nearby check