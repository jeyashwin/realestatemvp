from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import RequestToRentProperty, RequestToRentService, RequestToTourProperty
from .forms import RequestToRentPropertyForm, RequestToRentServiceForm, RequestToTourPropertyForm
from property.utils import studentAccessTest
from property.models import Property
from services.models import Service
from users.models import UserStudent
from notifications.models import Notification
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
                        identifier=form.instance.propertyObj.urlSlug,
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
                        identifier=form.instance.propertyObj.urlSlug,
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