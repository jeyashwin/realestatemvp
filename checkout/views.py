from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import RequestToRentProperty
from .forms import RequestToRentPropertyForm
from property.utils import studentAccessTest
from property.models import Property
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
                        fromObject=request.user.username,
                        toObject=form.instance.propertyObj.title,
                        notificationType='rentRequest',
                        identifier=form.instance.propertyObj.urlSlug
                    )
            messages.add_message(request, messages.SUCCESS, 'Request Sent Successfully.')
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error])
    return redirect('property:propertyDetail', slug=slug)
