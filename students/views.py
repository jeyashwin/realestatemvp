from django.shortcuts import render

# Create your views here.
def favourites(request):
    return render(request, 'students/favourites.html')

def roommates(request):
    return render(request, 'students/roommates.html')