from django.contrib import admin
from .models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick', 'sex', 'phone', 'birth')
    filter_list = ('birth', 'sex')
    search_fields = ('nick', 'phone')
    raw_id_fields = ['user', 'people']
