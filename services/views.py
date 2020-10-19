from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import *

# Create your views here.
def temp(request):
    return render(request, "services/single-service.html")

# class ServicesListView(ListView):
#     model = Services
#     template_name = "services/services.html"


# class ServicesDetailView(DetailView):
#     model = Services
#     template_name = "services/single-service.html"
