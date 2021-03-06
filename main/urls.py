from django.urls import path

from .views import statistic, a_reporting, addpolicy, redirect_login, unload_files, \
    register_user, mortgage, unload_mortgage, policy_edit, commission, accept, unload_accept, \
    commission_delete, upload_policy, upload_mortgage, add_type_channel_company, get_expenses, unload_expenses, \
    create_sale_report, get_sale_reports, base_upload, search

urlpatterns = [
    path('', redirect_login, name='redirect_login'),
    path('add_policy/', addpolicy, name='add_policy'),
    path('statistic/', statistic, name='statistic'),
    path('reporting/', a_reporting, name='reporting'),
    path('unload_files/', unload_files, name='unload_files'),
    path('register_user/', register_user, name='register_user'),
    path('mortgage/', mortgage, name='mortgage'),
    path('unload_mortgage/', unload_mortgage, name='unload_mortgage'),
    path('policy_edit/', policy_edit, name='policy_edit'),
    path('commission/', commission, name='commission'),
    path('accept/', accept, name='accept'),
    path('unload_accept/', unload_accept, name='unload_accept'),
    path('commission_delete/', commission_delete, name='commission_delete'),
    path('upload_policy/', upload_policy, name='upload_policy'),
    path('upload_mortgage/', upload_mortgage, name='upload_mortgage'),
    path('add_type_channel_company/', add_type_channel_company, name='add_type_channel_company'),
    path('expenses/', get_expenses, name='expenses'),
    path('unload_expenses/', unload_expenses, name='unload_expenses'),
    path('create_sale_report/', create_sale_report, name='create_sale_report'),
    path('sale_reports/', get_sale_reports, name='sale_reports'),
    path('base_upload/', base_upload, name='base_upload'),
    path('search/', search, name='search'),
]
