from django.contrib import admin
from .models import PolicyBase, Status, NameBase


@admin.register(Status)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PolicyBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'name', 'company', 'bso', 'date_end', 'manager']


@admin.register(NameBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']