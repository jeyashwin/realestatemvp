from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import AuthenticationForm

from .models import *
from users.forms import LandlordSignupForm, StudentSignupForm

# Create your views here.
class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"
    paginate_by = 10
    ordering = ['-createdDate']

    def get_queryset(self):
        serviceName = self.request.GET.get('serviceName', None)
        serviceObjects = super().get_queryset()
        if serviceName is not None and serviceName != "":
            serviceObjects = serviceObjects.filter(serviceName__icontains=serviceName)

        return serviceObjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AuthenticationForm
        context["LandlordSignupForm"] = LandlordSignupForm(label_suffix='')
        context["StudentSignupForm"] = StudentSignupForm(label_suffix='')
        num_pages = context["page_obj"].paginator.num_pages
        context["total_pages"] = [ i for i in range(1, num_pages+1)]
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/single-service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AuthenticationForm
        context["LandlordSignupForm"] = LandlordSignupForm(label_suffix='')
        context["StudentSignupForm"] = StudentSignupForm(label_suffix='')
        return context
    
