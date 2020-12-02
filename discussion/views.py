from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import generics, permissions

from students.permissions import IsStudentUserAccess, IsOwnerOfTheObject
from property.utils import studentAccessTest
from .serializers import *
from .models import *


# Create your views here.
class DiscussionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DiscussionPost
    template_name = "discussion/discussionList.html"
    ordering = ['-createdDate']

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):

        filters = self.request.GET.get('filter', None)
        if filters is not None:
            if filters == "mypost":
                return super().get_queryset().filter(student__user__user=self.request.user)
            else:
                try:
                    tag = get_object_or_404(DiscussionTag, pk=filters)
                    return super().get_queryset().filter(tags=tag)
                except Exception as e:
                    raise Http404

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = DiscussionTag.objects.all()
        return context


class DiscussionPostCreateView(generics.CreateAPIView):
    serializer_class = DiscussionPostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)

    def perform_create(self, serializer):
        studentObject = get_object_or_404(UserStudent, user__user=self.request.user)
        serializer.save(student=studentObject)


class DiscussionPostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscussionPostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = DiscussionPost.objects.all()


class DiscussionPostDetailView(generics.RetrieveAPIView):
    serializer_class = DiscussionPostDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)
    queryset = DiscussionPost.objects.all()


class DiscussionPostCommentCreateView(generics.CreateAPIView):
    serializer_class = DiscussionPostCommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)

    def perform_create(self, serializer):
        discussionObj = get_object_or_404(DiscussionPost, pk=self.kwargs.get('pk'))
        studentObject = get_object_or_404(UserStudent, user__user=self.request.user)
        serializer.save(discussionPost=discussionObj, student=studentObject)


class DiscussionPostCommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscussionPostCommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = DiscussionPostComment.objects.all()


class DiscussionCommentReplyCreateView(generics.CreateAPIView):
    serializer_class = DiscussionCommentReplySerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess)

    def perform_create(self, serializer):
        commentObj = get_object_or_404(DiscussionPostComment, pk=self.kwargs.get('pk'))
        studentObject = get_object_or_404(UserStudent, user__user=self.request.user)
        serializer.save(comment=commentObj, student=studentObject)


class DiscussionCommentReplyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscussionCommentReplySerializer
    permission_classes = (permissions.IsAuthenticated, IsStudentUserAccess, IsOwnerOfTheObject)
    queryset = DiscussionCommentReply.objects.all()


@login_required
@user_passes_test(studentAccessTest)
def DiscussionAddRemoveHeart(request, pk):
    DicussionObject = get_object_or_404(DiscussionPost, pk=pk)
    if request.method == "POST":
        studentObj = get_object_or_404(UserStudent, user__user=request.user)
        alreadyhearted = DicussionObject.heart.filter(user=studentObj.user).exists()
        if alreadyhearted:
            DicussionObject.heart.remove(studentObj)
            hearted = False
        else:
            DicussionObject.heart.add(studentObj)
            hearted = True
        DicussionObject.save()
        return JsonResponse({'hearted': hearted, 'total': DicussionObject.totalHearts()})
    return redirect('discussion:discussionList')