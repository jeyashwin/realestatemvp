"""realestatex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/defender/', include('defender.urls')),
    path('', include("users.urls", namespace='userApp')),
    path('',include("property.urls", namespace='propertyApp')),
    path('', include("students.urls", namespace='studentsApp')),
    path('', include("services.urls", namespace='servicesApp')),
    path('', include("checkout.urls", namespace='checkoutApp')),
    path('', include("notifications.urls", namespace='notificationApp')),
    path('', include("discussion.urls", namespace='discussionApp')),
    path('chat/', include("chat.urls", namespace='chatApp')),
    path('', include("resources.urls", namespace='resourcesApp')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
