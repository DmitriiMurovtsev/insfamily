from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('secretx/admin/', admin.site.urls),
    path('', include('main.urls')),
    path('prolongations/', include('prolongations.urls')),
    path('agents/', include('agents.urls')),
    path('', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
