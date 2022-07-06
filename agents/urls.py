from django.urls import path

from .views import issuance_bso, receivable, unload_receivable, unload_errors


urlpatterns = [
    path('issuance_bso/', issuance_bso, name='issuance_bso'),
    path('receivable/', receivable, name='receivable'),
    path('unload_receivable/', unload_receivable, name='unload_receivable'),
    path('unload_errors/', unload_errors, name='unload_errors'),
]
