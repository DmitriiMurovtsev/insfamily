from django.contrib import admin
from .models import User, Company, Channel, Client, Policy, Type, Bso, Bank, MortgagePolicy


class PolicyInline(admin.TabularInline):
    model = Policy
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    inlines = [PolicyInline]


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'client', 'user', 'company', 'channel']


@admin.register(Bso)
class PolicyBso(admin.ModelAdmin):
    list_display = ['id', 'series', 'number', 'date_at', 'user']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Type)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'middle_name', 'birthday', 'phone']
    inlines = [PolicyInline]


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(MortgagePolicy)
class MortgagePolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank', 'date_end', 'date_at']
