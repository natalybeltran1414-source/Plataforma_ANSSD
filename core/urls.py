from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('diagnostico/', views.diagnostico, name='diagnostico'),
    path('modulo/<int:modulo_id>/', views.modulo, name='modulo'),
    path('tutor/', views.tutor, name='tutor'),
    path('progreso/', views.progreso, name='progreso'),
    path('certificado/', views.generar_certificado, name='certificado'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),  # Nueva ruta
]