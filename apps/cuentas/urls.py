from django.urls import path
from .views import VistaLogin, VistaLogout, VistaDashboard

app_name = 'cuentas'

urlpatterns = [
    path('cuentas/login/', VistaLogin.as_view(), name='login'),
    path('cuentas/logout/', VistaLogout.as_view(), name='logout'),
    path('dashboard/', VistaDashboard.as_view(), name='dashboard'),
]
