from django.urls import path

from .views import status_change, upload_policy

urlpatterns = [
    path('status_change/', status_change, name='status_change'),
    path('upload_policy/', upload_policy, name='upload_policy'),
]
