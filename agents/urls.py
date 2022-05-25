from django.urls import path

from .views import issuance_bso, receivable


urlpatterns = [
    path('issuance_bso/', issuance_bso, name='issuance_bso'),
    path('receivable/', receivable, name='receivable'),
]
