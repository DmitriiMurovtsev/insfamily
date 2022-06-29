from django.urls import path

from .views import issuance_bso, receivable, unload_receivable, test_upload


urlpatterns = [
    path('issuance_bso/', issuance_bso, name='issuance_bso'),
    path('receivable/', receivable, name='receivable'),
    path('unload_receivable/', unload_receivable, name='unload_receivable'),
    path('test_upload/', test_upload, name='test_upload'),
]
