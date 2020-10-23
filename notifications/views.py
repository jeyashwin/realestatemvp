from django.shortcuts import render, get_object_or_404, redirect

from .models import Notification
# Create your views here.

def notification(request, pk):
    obj = get_object_or_404(Notification, pk=pk)

    if obj.notificationType == 'rentRequest':
        obj.viewed = True
        obj.save()
        return redirect('property:propertyDetail', slug=obj.identifier)
