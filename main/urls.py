from django.urls import path

from .views import statistic, a_reporting, addpolicy, redirect_login, unload_files, \
    register_user, bso_delete, mortgage, unload_mortgage, policy_edit, search_policy, commission, accept, unload_accept, \
    commission_delete, motivation, bonuses, bso_add, bso_agent, bso_stock

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
    path('search_policy/', search_policy, name='search_policy'),
    path('commission/', commission, name='commission'),
    path('accept/', accept, name='accept'),
    path('unload_accept/', unload_accept, name='unload_accept'),
    path('commission_delete/', commission_delete, name='commission_delete'),
    path('motivation/', motivation, name='motivation'),
    path('bonuses/', bonuses, name='bonuses'),
    path('bso_agent/', bso_agent, name='bso_agent'),
    path('bso_add/', bso_add, name='bso_add'),
    path('bso_stock/', bso_stock, name='bso_stock'),
    path('bso_delete/', bso_delete, name='bso_delete'),
]
