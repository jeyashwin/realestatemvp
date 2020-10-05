from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404

from property.utils import studentAccessTest
from property.models import Property
from users.models import UserStudent
from .models import Favourite

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


def roommates(request):
    return render(request, 'students/roommates.html')

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