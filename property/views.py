from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from django.http import JsonResponse
import pymongo
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy    

from users.models import UserLandLord , UserStudent
from .models import Property, PostQuestion, PostAnswer
from .forms import PropertyForm, PropertyImageFormset, PropertyVideoFormset, PropertyFilterSortForm

# Create your views here.
data = pd.read_csv("ny_data.csv")
data = data.dropna(subset=["CITY"])

class MONGO_CONFS:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["property_data"]
    mycol = mydb["comments"]


def decoder(request,name):
    if request.method == "GET":
        print(name,"REQUEST")
        # print(request.name,"REQ NAME")

def search(request,text):
    print(text,"TEXT")
    wanted_columns = ["PROPERTY TYPE","ADDRESS","CITY","ZIP OR POSTAL CODE","PRICE","BEDS","BATHS","LOCATION","SQUARE FEET"]
    if isinstance(text,int):
        return data[data["ZIP OR POSTAL CODE"] == text][wanted_columns].to_dict()
    if text.lower() in [i.lower() for i in data['CITY'].unique()]:
        exact_txt = [val for val in  list(data['CITY'].unique()) if val.lower() == text]
        return JsonResponse(data[data["CITY"] == exact_txt[0]].to_dict())
    else:
        return JsonResponse({"error":0})

@csrf_exempt
def add_comment(request):
    print(request.POST["property-comment"],dict(request.POST))
    comments = MONGO_CONFS.mycol
    comments.insert_one({"user_id": request.POST['user_id'],
                         "property_id": request.POST['property_id'],
                         "comment": request.POST['property-comment'], "sequence": 0})
    return render(request,"templates/single-property.html",{})


#Property App views starts from here

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
        return Property.objects.filter(landlord__user__user=self.request.user)


class PropertyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Property
    template_name = "property/properties.html"
    ordering = ['-createdDate']
    paginate_by = 10
    form_class = PropertyFilterSortForm

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):
        filterSortForm = PropertyFilterSortForm(self.request.GET)
        print(filterSortForm)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterSortForm"] = PropertyFilterSortForm()
        num_pages = context["page_obj"].paginator.num_pages
        context["total_pages"] = [ i for i in range(1, num_pages+1)]
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


def studentAccessTest(user):
    try:
        if not user.usertype.is_student:
            raise Http404
        else:
            return True
    except:
        raise Http404

def landlordAccessTest(user):
    try:
        if not user.usertype.is_landlord:
            raise Http404
        else:
            return True
    except:
        raise Http404

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
        return JsonResponse({'question': question})

    return redirect('property:propertyDetail', slug)

@login_required
@user_passes_test(landlordAccessTest)
def PostAnswerView(request, slug, pk):
    prop = get_object_or_404(Property, urlSlug=slug)
    if prop.landlord.user.user == request.user:
        if request.method == "POST":
            answer = request.POST.get("prop-answer", None)
            if answer is not None and answer != "":
                ques = get_object_or_404(PostQuestion, pk=pk)
                ansObject = PostAnswer.objects.create(question=ques, answer=answer)
        return redirect('property:propertyDetail', slug)
    else:
        raise Http404
