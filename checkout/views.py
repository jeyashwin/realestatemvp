from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import RequestToRentProperty, RequestToRentService, RequestToTourProperty
from .forms import RequestToRentPropertyForm, RequestToRentServiceForm, RequestToTourPropertyForm
from property.utils import studentAccessTest, landlordAccessTest
from property.models import Property
from services.models import Service
from users.models import UserStudent
from notifications.models import Notification
from rest_framework import generics, viewsets
from .serializers import RequestToRentPropertySerializer, RequestToRentServiceSerializer, RequestToTourPropertySerializer
# Create your views here.

@login_required
@user_passes_test(studentAccessTest)
def RequestToRentPropertyCreateView(request, slug):
    form = RequestToRentPropertyForm()
    if request.method == 'POST':
        form = RequestToRentPropertyForm(request.POST)
        form.instance.propertyObj = get_object_or_404(Property, urlSlug=slug)
        form.instance.studentObj = get_object_or_404(UserStudent, user__user=request.user)
        if form.is_valid():
            form.save()
            notf = Notification.objects.create(
                        fromUser=request.user,
                        toUser=form.instance.propertyObj.landlord.user.user,
                        notificationType='rentRequest',
                        content=form.instance.propertyObj.title,
                        identifier=form.instance.pk,
                    )
            messages.add_message(request, messages.SUCCESS, 'Rent Request Sent Successfully.')
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])
    return redirect('property:propertyDetail', slug=slug)


@login_required
@user_passes_test(studentAccessTest)
def RequestToTourPropertyCreateView(request, slug):
    form = RequestToTourPropertyForm()
    if request.method == 'POST':
        form = RequestToTourPropertyForm(request.POST)
        form.instance.propertyObj = get_object_or_404(Property, urlSlug=slug)
        form.instance.studentObj = get_object_or_404(UserStudent, user__user=request.user)
        if form.is_valid():
            form.save()
            notf = Notification.objects.create(
                        fromUser=request.user,
                        toUser=form.instance.propertyObj.landlord.user.user,
                        notificationType='tourRequest',
                        content=form.instance.propertyObj.title,
                        identifier=form.instance.pk,
                    )
            messages.add_message(request, messages.SUCCESS, 'Tour Request Sent Successfully.')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    return redirect('property:propertyDetail', slug=slug)


@login_required
@user_passes_test(studentAccessTest)
def RequestToRentServiceCreateView(request, pk):
    form =RequestToRentServiceForm()
    if request.method == 'POST':
        form = RequestToRentServiceForm(request.POST)
        serviceObj = get_object_or_404(Service, pk=pk)
        studentObj = get_object_or_404(UserStudent, user__user=request.user)
        form.instance.serviceObj = serviceObj
        form.instance.studentObj = studentObj
        if form.is_valid():
            form.save()
            # adminUser = get_user_model().objects.get(is_superuser=True)
            # notf = Notification.objects.create(
            #                 fromUser=request.user,
            #                 toUser=adminUser,
            #                 notificationType='serviceRequest',
            #                 content=serviceObj.serviceName,
            #                 identifier=serviceObj.pk,
            #             )
            messages.add_message(request, messages.SUCCESS, 'Request Sent Successfully.')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    return redirect('services:servicesDetail', pk=pk)

@login_required
@user_passes_test(landlordAccessTest)
def myrequest(request):
    rentRequest = RequestToRentProperty.objects.filter(propertyObj__landlord__user__user=request.user).order_by('-createdDate')
    tourRequest = RequestToTourProperty.objects.filter(propertyObj__landlord__user__user=request.user).order_by('-createdDate')
    context = {
        'rentRequest': rentRequest,
        'tourRequest': tourRequest
    }
    return render(request, 'checkout/myrequest.html', context=context)


class RequestToRentPropertyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RequestToRentProperty
    template_name = "checkout/myrequestrentview.html"

    def test_func(self):
        try:
            return self.request.user.usertype.is_landlord
        except:
            raise Http404


class RequestToTourPropertyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RequestToTourProperty
    template_name = "checkout/myrequesttourview.html"

    def test_func(self):
        try:
            return self.request.user.usertype.is_landlord
        except:
            raise Http404

class RequestToTourPropertyListCreate(generics.ListCreateAPIView):
    queryset = RequestToTourProperty.objects.all()
    serializer_class = RequestToTourPropertySerializer

class RequestToTourPropertyViewSet(viewsets.ModelViewSet):
    queryset = RequestToTourProperty.objects.all()
    serializer_class = RequestToTourPropertySerializer

class RequestToRentPropertyListCreate(generics.ListCreateAPIView):
    queryset = RequestToRentProperty.objects.all()
    serializer_class = RequestToRentPropertySerializer

class RequestToRentPropertyViewSet(viewsets.ModelViewSet):
    queryset = RequestToRentProperty.objects.all()
    serializer_class = RequestToRentPropertySerializer

class RequestToRentServiceListCreate(generics.ListCreateAPIView):
    queryset = RequestToRentService.objects.all()
    serializer_class = RequestToRentServiceSerializer

class RequestToRentServiceViewSet(viewsets.ModelViewSet):
    qqueryset = RequestToRentService.objects.all()
    serializer_class = RequestToRentServiceSerializer
