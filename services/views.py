from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import *

# Create your views here.
class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"
    paginate_by = 10
    ordering = ['-createdDate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_pages = context["page_obj"].paginator.num_pages
        context["total_pages"] = [ i for i in range(1, num_pages+1)]
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/single-service.html"
