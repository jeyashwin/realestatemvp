from django.contrib import admin
from .models import Favourite

# Register your models here.
@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ["id", "student"]