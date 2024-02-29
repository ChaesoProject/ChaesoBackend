from django.contrib import admin
from django.urls import path, include
from core.urls import urlpatterns as core_urls


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('', include(core_urls)),
    # Djoser
    path('api/v1/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
]
