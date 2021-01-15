from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from .models import *
from checkout.forms import RequestToRentServiceForm
from .models import Service
from .serializers import ServiceSerializer, ServiceImageSerializer
from rest_framework import generics, viewsets


# Create your views here.
class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = "services/services.html"
    paginate_by = 25
    ordering = ['-createdDate']

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_queryset(self):
        serviceName = self.request.GET.get('serviceName', None)
        serviceObjects = super().get_queryset()
        if serviceName is not None and serviceName != "":
            serviceObjects = serviceObjects.filter(serviceName__icontains=serviceName)

        return serviceObjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_pages = context["page_obj"].paginator.num_pages
        context["total_pages"] = [ i for i in range(1, num_pages+1)]
        return context


class ServiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Service
    template_name = "services/single-service.html"

    def test_func(self):
        try:
            return self.request.user.usertype.is_student
        except:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RequestToRentServiceForm(initial={
                                'first_name': self.request.user.first_name,
                                'last_name': self.request.user.last_name,
                                'phone_number': self.request.user.usertype.userstudent.phone,
                                'email': self.request.user.email
                            })
        return context

class ServiceListCreate(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceImageListCreate(generics.ListCreateAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer

class ServiceImageViewSet(viewsets.ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer

