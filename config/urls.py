from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.cuentas.urls')),
    path('personas/', include('apps.personas.urls')),
    path('', include('apps.programas.urls')),
    path('nombramientos/', include('apps.nombramientos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
