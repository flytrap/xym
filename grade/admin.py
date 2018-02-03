from django.contrib import admin
from .models import People, Grade


# Register your models here.
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'desc')


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'master_name', 'birth_death')
    search_fields = ('name', 'master_name', 'desc')
    list_filter = ('grade', 'master_name')
