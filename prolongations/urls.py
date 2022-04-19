from django.urls import path

from .views import status_change, upload_policy, get_statistic

urlpatterns = [
    path('status_change/', status_change, name='status_change'),
    path('upload_policy/', upload_policy, name='upload_policy'),
    path('statistic_p/', get_statistic, name='statistic_p'),
]
