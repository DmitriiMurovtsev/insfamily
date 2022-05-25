from django.contrib import admin
from .models import Agent, Bso, PolicyAgents


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'storage_time', 'date_at']


@admin.register(Bso)
class BsoAdmin(admin.ModelAdmin):
    list_display = ['id', 'series', 'number', 'agent', 'date_add', 'date_at']


@admin.register(PolicyAgents)
class PolicyAgentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'policy', 'agent']
