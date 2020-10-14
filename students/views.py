from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from rest_framework import generics, permissions

from property.utils import studentAccessTest
from property.models import Property
from users.models import UserStudent
from .models import Favourite, RoommatePost, PostComment, CommentReply, Preference
from .serializers import RoommatePostDetailSerializer, PostCommentSerializer, \
                            CommentReplySerializer
from .permissions import IsStudentUserAccess, IsOwnerOfTheObject
from .forms import RoommatePostForm

# Create your views here.

class FavouriteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Favourite
    template_name = "students/favourites.html"
    # ordering = ['-properties']

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):
        return Favourite.objects.filter(student__user__user=self.request.user)


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = RoommatePostForm
    model = RoommatePost
    success_url = "/"
    template_name = 'students/roommates.html'

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def form_valid(self, form):
        form.instance.student = get_object_or_404(UserStudent, user__user=self.request.user)
        form.instance.preference = get_object_or_404(Preference, preferenceSlug=self.kwargs.get('preference'))
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('students:roommatesPreference', kwargs={'preference':self.kwargs.get('preference')})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = RoommatePostForm
    model = RoommatePost
    success_url = "/roommates/"
    template_name = 'students/roommates.html'

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(student__user__user=self.request.user)


class RoommatesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RoommatePost
    template_name = "students/roommates.html"
    ordering = ['-createdDate']

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):
        pre = self.kwargs.get('preference', None)
        if pre is not None:
            preference = get_object_or_404(Preference, preferenceSlug=pre)
            return super().get_queryset().filter(preference=preference)
        else:
            return super().get_queryset().filter(student__user__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["preferences"] = Preference.objects.all()
        pre = self.kwargs.get('preference', None)
        if pre is not None:
            context["form"] = RoommatePostForm()
            context["currentpreferences"] = get_object_or_404(Preference, preferenceSlug=pre)
        return context 


# class RoommatesPostUpdateView(generics.RetrieveUpdateAPIView):
#     serializer_class = RoommatePostSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
#     queryset = RoommatePost.objects.all()


class RoommatesPostDetailView(generics.RetrieveAPIView):
    serializer_class = RoommatePostDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)
    queryset = RoommatePost.objects.all()


class RoommatesPostDeleteView(generics.DestroyAPIView):
    serializer_class = RoommatePostDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = RoommatePost.objects.all()


class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)

    def perform_create(self, serializer):
        postObj = get_object_or_404(RoommatePost, pk=self.kwargs.get('pk'))
        studentObject = get_object_or_404(UserStudent, user__user=self.request.user)
        serializer.save(roomatePost=postObj, student=studentObject)

class PostCommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = PostComment.objects.all()

class CommentReplyCreateView(generics.CreateAPIView):
    serializer_class = CommentReplySerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)

    def perform_create(self, serializer):
        commentObj = get_object_or_404(PostComment, pk=self.kwargs.get('pk'))
        studentObject = get_object_or_404(UserStudent, user__user=self.request.user)
        serializer.save(comment=commentObj, student=studentObject)


class CommentReplyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentReplySerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = CommentReply.objects.all()


@login_required
@user_passes_test(studentAccessTest)
def AddFavourite(request, slug):
    added = True
    if request.method == "POST":
        student = Favourite.objects.filter(student__user__user=request.user).exists()
        propObject = get_object_or_404(Property, urlSlug=slug)
        if student:
            favouriteObject = Favourite.objects.get(student__user__user=request.user)
            propExists = favouriteObject.properties.filter(pk=propObject.pk).exists()
            if not propExists:
                favouriteObject.properties.add(propObject)
                favouriteObject.save()
            else:
                added = False
        else:
            studObject = get_object_or_404(UserStudent, user__user=request.user)
            favouriteObject = Favourite.objects.create(student=studObject)
            favouriteObject.properties.add(propObject)
            favouriteObject.save()
        return JsonResponse({'added': added})
    return redirect('property:propertyDetail', slug)

@login_required
@user_passes_test(studentAccessTest)
def RemoveFavourite(request, slug):
    removed = True
    if request.method == "POST":
        student = Favourite.objects.filter(student__user__user=request.user).exists()
        propObject = get_object_or_404(Property, urlSlug=slug)
        if student:
            favouriteObject = Favourite.objects.get(student__user__user=request.user)
            propExists = favouriteObject.properties.filter(pk=propObject.pk).exists()
            if propExists:
                favouriteObject.properties.remove(propObject)
                favouriteObject.save()
            else:
                removed = False
        else:
            raise Http404
        return JsonResponse({'removed': removed})
    return redirect('property:propertyDetail', slug)