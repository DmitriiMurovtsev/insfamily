from django.urls import path

from .views import issuance_bso, receivable, unload_receivable


urlpatterns = [
    path('issuance_bso/', issuance_bso, name='issuance_bso'),
    path('receivable/', receivable, name='receivable'),
    path('unload_receivable/', unload_receivable, name='unload_receivable'),
]
