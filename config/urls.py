from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('', include('apps.cuentas.urls')),
    path('personas/', include('apps.personas.urls')),
    path('', include('apps.programas.urls')),
    path('nombramientos/', include('apps.nombramientos.urls')),
    path('tesis/', include('apps.tesis.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
