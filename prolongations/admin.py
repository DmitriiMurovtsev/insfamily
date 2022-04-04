from django.contrib import admin
from .models import PolicyOnProlongation, Status


@admin.register(PolicyOnProlongation)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'policy', 'client', 'month', 'policy_new', 'status']


@admin.register(Status)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'extended']
