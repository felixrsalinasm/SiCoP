from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import render

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE


def vista_403(request, exception):
    return render(request, '403.html', status=403)


def vista_404(request, exception):
    return render(request, '404.html', status=404)


def vista_500(request):
    return render(request, '500.html', status=500)


urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('', include('apps.cuentas.urls')),
    path('personas/', include('apps.personas.urls')),
    path('', include('apps.programas.urls')),
    path('nombramientos/', include('apps.nombramientos.urls')),
    path('tesis/', include('apps.tesis.urls')),
    path('historial/', include('apps.historial.urls')),
]

handler403 = vista_403
handler404 = vista_404
handler500 = vista_500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
