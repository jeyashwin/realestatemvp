# import pandas as pd
# import pymongo
# from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.db.models.functions import Distance
from django.contrib import messages
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.db import transaction
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy

from users.models import UserLandLord , UserStudent
from .models import Property, PostQuestion, PostAnswer, Amenities
from .utils import studentAccessTest, landlordAccessTest
from .forms import PropertyForm, PropertyImageFormset, PropertyVideoFormset, PropertyFilterSortForm
from checkout.forms import RequestToRentPropertyForm, RequestToTourPropertyForm
from notifications.models import Notification

# Create your views here.
# data = pd.read_csv("ny_data.csv")
# data = data.dropna(subset=["CITY"])

# class MONGO_CONFS:
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["property_data"]
#     mycol = mydb["comments"]


# def decoder(request,name):
#     if request.method == "GET":
#         print(name,"REQUEST")
#         # print(request.name,"REQ NAME")

# def search(request,text):
#     print(text,"TEXT")
#     wanted_columns = ["PROPERTY TYPE","ADDRESS","CITY","ZIP OR POSTAL CODE","PRICE","BEDS","BATHS","LOCATION","SQUARE FEET"]
#     if isinstance(text,int):
#         return data[data["ZIP OR POSTAL CODE"] == text][wanted_columns].to_dict()
#     if text.lower() in [i.lower() for i in data['CITY'].unique()]:
#         exact_txt = [val for val in  list(data['CITY'].unique()) if val.lower() == text]
#         return JsonResponse(data[data["CITY"] == exact_txt[0]].to_dict())
#     else:
#         return JsonResponse({"error":0})


#Property App views starts from here

def get_or_create_amenity(tempAmenity):
    if tempAmenity:
        tempAmenity = tempAmenity.capitalize()
        # print(tempAmenity)
        return Amenities.objects.get_or_create(amenityType=tempAmenity)
    return None


class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Property
    template_name = "property/submit-property.html"
    form_class = PropertyForm

    def test_func(self):
        try:
            return self.request.user.usertype.is_landlord
        except:
            raise Http404

    def form_valid(self, form):
        context = self.get_context_data()
        imageForm = context['imageForm']
        videoForm = context["videoForm"]
        with transaction.atomic():
            if imageForm.is_valid() and videoForm.is_valid():
                form.instance.landlord = UserLandLord.objects.get(user__user=self.request.user)
                self.object = form.save()
                imageForm.instance = self.object
                imageForm.save()
                videoForm.instance = self.object
                videoForm.save()
                amenity1 = get_or_create_amenity(form.cleaned_data.get('amenity1', None))
                amenity2 = get_or_create_amenity(form.cleaned_data.get('amenity2', None))
                amenity3 = get_or_create_amenity(form.cleaned_data.get('amenity3', None))
                amenity4 = get_or_create_amenity(form.cleaned_data.get('amenity4', None))
                amenity5 = get_or_create_amenity(form.cleaned_data.get('amenity5', None))
                amenity6 = get_or_create_amenity(form.cleaned_data.get('amenity6', None))
                if amenity1:
                    form.instance.amenities.add(amenity1[0].pk)
                if amenity2:
                    form.instance.amenities.add(amenity2[0].pk)
                if amenity3:
                    form.instance.amenities.add(amenity3[0].pk)
                if amenity4:
                    form.instance.amenities.add(amenity4[0].pk)
                if amenity5:
                    form.instance.amenities.add(amenity5[0].pk)
                if amenity6:
                    form.instance.amenities.add(amenity6[0].pk)
            else:
                return super().form_invalid(form)
                print(imageForm.errors)
                print(videoForm.errors)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["imageForm"] = PropertyImageFormset(self.request.POST, self.request.FILES)
            context["videoForm"] = PropertyVideoFormset(self.request.POST, self.request.FILES)
        else:
            context["imageForm"] = PropertyImageFormset()
            context["videoForm"] = PropertyVideoFormset()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('property:propertyManage')


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    template_name = "property/submit-property.html"
    form_class = PropertyForm
    slug_field = "urlSlug"

    def get_queryset(self):
        return Property.objects.filter(landlord__user__user=self.request.user)
    
    def form_valid(self, form):
        context = self.get_context_data()
        imageForm = context['imageForm']
        videoForm = context["videoForm"]
        with transaction.atomic():
            form.instance.landlord = UserLandLord.objects.get(user__user=self.request.user)
            self.object = form.save()
            if imageForm.is_valid() and videoForm.is_valid():
                imageForm.instance = self.object
                imageForm.save()
                videoForm.instance = self.object
                videoForm.save()

                form.instance.amenities.clear()
                amenity1 = get_or_create_amenity(form.cleaned_data.get('amenity1', None))
                amenity2 = get_or_create_amenity(form.cleaned_data.get('amenity2', None))
                amenity3 = get_or_create_amenity(form.cleaned_data.get('amenity3', None))
                amenity4 = get_or_create_amenity(form.cleaned_data.get('amenity4', None))
                amenity5 = get_or_create_amenity(form.cleaned_data.get('amenity5', None))
                amenity6 = get_or_create_amenity(form.cleaned_data.get('amenity6', None))
                if amenity1:
                    form.instance.amenities.add(amenity1[0].pk)
                if amenity2:
                    form.instance.amenities.add(amenity2[0].pk)
                if amenity3:
                    form.instance.amenities.add(amenity3[0].pk)
                if amenity4:
                    form.instance.amenities.add(amenity4[0].pk)
                if amenity5:
                    form.instance.amenities.add(amenity5[0].pk)
                if amenity6:
                    form.instance.amenities.add(amenity6[0].pk)
            else:
                return super().form_invalid(form)
                print(imageForm.errors)
                print(videoForm.errors)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["imageForm"] = PropertyImageFormset(self.request.POST, self.request.FILES, instance=self.object)
            context["videoForm"] = PropertyVideoFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["imageForm"] = PropertyImageFormset(instance=self.object)
            context["videoForm"] = PropertyVideoFormset(instance=self.object)
        return context

    def get_success_url(self, **kwargs):
        # return reverse_lazy('property:propertyUpdate', kwargs={'slug':self.object.urlSlug})
        return reverse_lazy('property:propertyManage')


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = "property/propertyDelete.html"
    slug_field = "urlSlug"
    success_url = "/"

    def get_queryset(self):
        return Property.objects.filter(landlord__user__user=self.request.user)


class LandlordManageProperty(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Property
    template_name = "property/manage-properties.html"
    ordering = ['-updatedDate']

    def test_func(self):
        try:
            return self.request.user.usertype.is_landlord
        except:
            raise Http404

    def get_queryset(self):
        return super().get_queryset().filter(landlord__user__user=self.request.user)
        

class PropertyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Property
    template_name = "property/properties.html"
    paginate_by = 25
    form_class = PropertyFilterSortForm

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):
        longitude = -73.12082590786636
        latitude = 40.91638132127517
        userlocation = Point(longitude, latitude, srid=4326)
        
        filterSortForm = PropertyFilterSortForm(data=self.request.GET)
        propObjects = super().get_queryset().annotate(distance=Distance(userlocation, 'location')).order_by('distance')
        propObjects = propObjects.filter(isleased=False)
        if filterSortForm.is_valid():
            room = filterSortForm.cleaned_data.get('room', None)
            occp = filterSortForm.cleaned_data.get('occp', None)
            bath = filterSortForm.cleaned_data.get('bath', None)
            minPri = filterSortForm.cleaned_data.get('minPri', None)
            maxPri = filterSortForm.cleaned_data.get('maxPri', None)
            # amenities = filterSortForm.cleaned_data.get('amenities', None)
            sort = filterSortForm.cleaned_data.get('sort', None)
            disPro = filterSortForm.cleaned_data.get('disPro', None)
            disAmen = filterSortForm.cleaned_data.get('disAmen', None)
            if disPro is not None:
                propObjects = propObjects.filter(distance__lte=D(mi=disPro+0.05).m)
            if disAmen is not None:
                propObjects = propObjects.filter(averageDistance__lte=disAmen)
            if room is not None and room != []:
                room = [ int(i) for i in room ]
                if 4 not in room:
                    propObjects = propObjects.filter(rooms__in=room)
                else:
                    room.remove(4)
                    if room != []:
                        propObjects1 = propObjects.filter(rooms__gte=4)
                        propObjects = propObjects.filter(rooms__in=room)
                        propObjects = propObjects.union(propObjects1)
                    else:
                        propObjects = propObjects.filter(rooms__gte=4)
            if occp is not None and occp != []:
                occp = [ int(i) for i in occp ]
                if 4 not in occp:
                    propObjects = propObjects.filter(occupants__in=occp)
                else:
                    occp.remove(4)
                    if occp != []:
                        propObjects1 = propObjects.filter(occupants__gte=4)
                        propObjects = propObjects.filter(occupants__in=occp)
                        propObjects = propObjects.union(propObjects1)
                    else:
                        propObjects = propObjects.filter(occupants__gte=4)
            if bath is not None and bath != []:
                bath = [ int(i) for i in bath ]
                if 4 not in bath:
                    propObjects = propObjects.filter(bathrooms__in=bath)
                else:
                    bath.remove(4)
                    if bath != []:
                        propObjects1 = propObjects.filter(bathrooms__gte=4)
                        propObjects = propObjects.filter(bathrooms__in=bath)
                        propObjects = propObjects.union(propObjects1)
                    else:
                        propObjects = propObjects.filter(bathrooms__gte=4)
            if minPri is not None:
                propObjects = propObjects.filter(rentPerPerson__gte=minPri)
            if maxPri is not None:
                propObjects = propObjects.filter(rentPerPerson__lte=maxPri)
            # if amenities is not None and amenities:
            #     propObjects = propObjects.filter(amenities__in=amenities).distinct()
            if sort is not None:
                if sort == "p_low_hi":
                    propObjects = propObjects.order_by("rentPerPerson")
                if sort == "p_hi_low":
                    propObjects = propObjects.order_by("-rentPerPerson")
                if sort == "room":
                    propObjects = propObjects.order_by("-rooms")
                if sort == "bath":
                    propObjects = propObjects.order_by("-bathrooms")
                # if sort == "sqft":
                #     propObjects = propObjects.order_by("-sqft")
        else:
            print(filterSortForm)
        return propObjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterSortForm"] = PropertyFilterSortForm(data=self.request.GET)
        num_pages = context["page_obj"].paginator.num_pages
        context["total_pages"] = [ i for i in range(1, num_pages+1)]
        context["total_count"] = self.object_list.count()
        return context


class PropertyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Property
    template_name = "property/single-property.html"
    slug_field = 'urlSlug'

    def test_func(self):
        try:
            if self.request.user.usertype:
                return True
        except:
            raise Http404

    def get_queryset(self):
        if self.request.user.usertype.is_landlord:
            return Property.objects.filter(landlord__user__user=self.request.user)
        else:
            return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alreadyLiked"] = self.object.likes.filter(user__user=self.request.user).exists()
        context["alreadyDisLiked"] = self.object.dislikes.filter(user__user=self.request.user).exists()
        # context["alreadyFavorite"] = self.object.favorite_set.filter(student__user__user=self.request.user).exists()
        if self.request.user.usertype.is_student:
            context["form"] = RequestToRentPropertyForm()
            context["tourForm"] = RequestToTourPropertyForm()
        return context  


@login_required
@user_passes_test(studentAccessTest)
def LikesDisLikesView(request, slug):
    if request.method == "POST":
        likePress = request.POST.get("like", "None")
        dislikePress = request.POST.get("dislike", "None")
        propObject = get_object_or_404(Property, urlSlug=slug)
        studObject = get_object_or_404(UserStudent, user__user=request.user)
        alreadyLiked = propObject.likes.filter(user=studObject.user).exists()
        alreadyDisliked = propObject.dislikes.filter(user=studObject.user).exists()
        liked, disliked = 0, 0
        if alreadyLiked:
            if likePress == "1":
                propObject.likes.remove(studObject)
            elif dislikePress == "1":
                propObject.likes.remove(studObject)
                propObject.dislikes.add(studObject)
                disliked = 1
        elif alreadyDisliked:
            if likePress == "1":
                propObject.dislikes.remove(studObject)
                propObject.likes.add(studObject)
                liked = 1
            elif dislikePress == "1":
                propObject.dislikes.remove(studObject)
        elif not(alreadyLiked and alreadyDisliked):
            if likePress == "1":
                propObject.likes.add(studObject)
                liked = 1
            elif dislikePress == "1":
                propObject.dislikes.add(studObject)
                disliked = 1
        propObject.save()
        likecount = propObject.totalLikes()
        dislikecount = propObject.totalDislikes()
        return JsonResponse({
                "liked": liked, 
                "disliked": disliked, 
                "likecount": likecount,
                "dislikecount": dislikecount,
                })

    return redirect('property:propertyList')

@login_required
@user_passes_test(studentAccessTest)
def PostQuestionView(request, slug):
    if request.method == "POST":
        question = request.POST.get("question", None)
        if question is not None and question != "":
            prop = get_object_or_404(Property, urlSlug=slug)
            stud = get_object_or_404(UserStudent, user__user=request.user)
            quesObject = PostQuestion.objects.create(propKey=prop, student=stud, question=question)
            notfy = Notification.objects.create(
                        fromUser=request.user,
                        toUser=prop.landlord.user.user,
                        notificationType='question',
                        content=prop.title,
                        identifier=prop.urlSlug,
                    )
        return JsonResponse({'question': question})

    return redirect('property:propertyDetail', slug)

@login_required
@user_passes_test(landlordAccessTest)
def PostAnswerView(request, pk):
    ques = get_object_or_404(PostQuestion, pk=pk)
    if ques.propKey.landlord.user.user == request.user:
        if request.method == "POST":
            answer = request.POST.get("prop-answer", None)
            if answer is not None and answer != "":
                ansObject = PostAnswer.objects.create(question=ques, answer=answer)
                notfy = Notification.objects.create(
                        fromUser=request.user,
                        toUser=ques.student.user.user,
                        notificationType='answered',
                        content=ques.question,
                        identifier=ques.propKey.urlSlug,
                    )
                return JsonResponse({'answer': answer})
        return redirect('property:propertyDetail', ques.propKey.urlSlug)
    else:
        raise Http404

@login_required
@user_passes_test(landlordAccessTest)
def PostQuestionDeleteView(request, pk):
    ques = get_object_or_404(PostQuestion, pk=pk)
    if ques.propKey.landlord.user.user == request.user:
        if request.method == "POST":
            notfy = Notification.objects.create(
                    fromUser=request.user,
                    toUser=ques.student.user.user,
                    notificationType='deletedQuestion',
                    content=ques.question,
                    identifier=ques.propKey.urlSlug,
                )
            ques.delete()
            return JsonResponse({'deleted': True})
        return redirect('property:propertyDetail', ques.propKey.urlSlug)
    else:
        raise Http404

@login_required
@user_passes_test(landlordAccessTest)
def VaccantChangeView(request, slug):
    if request.method == "POST":
        propObject = get_object_or_404(Property, urlSlug=slug)
        #add check point if the same owner is changing
        # print(request.POST)
        leaseStatus = request.POST.get('leasestatus', None)
        leaseStart = request.POST.get('leasestartdate', None)
        leaseEnd = request.POST.get('leaseenddate', None)
        if leaseStatus:
            if leaseStatus == 'lease':
                if leaseStart == '' or leaseStart is None or leaseEnd == '' or leaseEnd is None:
                    messages.add_message(request, messages.ERROR, 'Lease Start and End date is required')
                else:
                    propObject.isleased = True
                    propObject.leaseStart = leaseStart
                    propObject.leaseEnd = leaseEnd
                    propObject.save()
                    messages.add_message(request, messages.SUCCESS, 'Property status changed to Leased.')
            elif leaseStatus == 'vaccant':
                propObject.isleased = False
                if propObject.leaseStart:
                    propObject.leaseStart = None
                if propObject.leaseEnd:
                    propObject.leaseEnd = None
                propObject.save()
                messages.add_message(request, messages.SUCCESS, 'Property status changed to Vaccant.')
            else:
                messages.add_message(request, messages.ERROR, 'Not a valid option!')
    return redirect('property:propertyManage')

@login_required
@user_passes_test(studentAccessTest)
def TagFriendsView(request, slug):
    if request.method == "POST":
        tagFriend = request.POST.get("tagFriend", None)
        if tagFriend is not None and tagFriend != "":
            prop = get_object_or_404(Property, urlSlug=slug)
            stud = get_object_or_404(UserStudent, user__user__username=tagFriend)
            notfy = Notification.objects.create(
                        fromUser=request.user,
                        toUser=stud.user.user,
                        notificationType='tagFriend',
                        content=prop.title,
                        identifier=prop.urlSlug,
                    )
            messages.add_message(request, messages.SUCCESS, f'Tagged {tagFriend} successfully!')
    return redirect('property:propertyList')