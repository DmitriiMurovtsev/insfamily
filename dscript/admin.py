from django.contrib import admin
from .models import Script, Step, Answer, Stage


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'script']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'step']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
