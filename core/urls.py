from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomUserViewSet


router = SimpleRouter()
router.register('customuser', CustomUserViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
