from django.urls import path

from .views import create_script, show_script, show_step


urlpatterns = [
    path('create_script/', create_script, name='create_script'),
    path('show_script/', show_script, name='show_script'),
    path('show_step/', show_step, name='show_step'),
]
