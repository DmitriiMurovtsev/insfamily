from django.urls import path

from .views import status_change, upload_policy, new_statistics

urlpatterns = [
    path('status_change/', status_change, name='status_change'),
    path('upload_policy/', upload_policy, name='upload_policy'),
    path('new_statistics/', new_statistics, name='new_statistics'),
]
