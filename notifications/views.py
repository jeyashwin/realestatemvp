from django.shortcuts import render, get_object_or_404, redirect

from .models import Notification
# Create your views here.

def notification(request, pk):
    obj = get_object_or_404(Notification, pk=pk)

    if obj.notificationType == 'rentRequest' or obj.notificationType == 'tourRequest' or obj.notificationType == 'question' or obj.notificationType == 'answered':
        obj.viewed = True
        obj.save()
        return redirect('property:propertyDetail', slug=obj.identifier)

    if obj.notificationType == 'serviceRequest':
        obj.viewed = True
        obj.save()
        return redirect('services:servicesDetail', pk=obj.identifier)
    
    if obj.notificationType == 'deletedQuestion':
        obj.viewed = True
        obj.save()
        return redirect('property:propertyDetail', slug=obj.identifier)
