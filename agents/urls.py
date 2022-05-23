from django.urls import path

from .views import add_agent, issuance_bso, get_statistic, accept


urlpatterns = [
    path('add_agent/', add_agent, name='add_agent'),
    path('issuance_bso/', issuance_bso, name='issuance_bso'),
    path('get_statistic/', get_statistic, name='get_statistic'),
    path('accept/', accept, name='accept_agent'),
]
