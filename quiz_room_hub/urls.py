from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("api/", include("authuser.urls", namespace="authuser")),
                  path("api/", include("account.urls", namespace="account")),
                  path("api/", include("classroom.urls", namespace="classroom")),
                  path("api/", include("quiz.urls.urls", namespace="quiz")),
                  path("api/", include("post.urls", namespace="post")),
                  path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
