from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('diagnostico/', views.diagnostico, name='diagnostico'),
    path('modulo/<int:modulo_id>/', views.modulo, name='modulo'),
    path('tutor/', views.tutor, name='tutor'),
    path('progreso/', views.progreso, name='progreso'),
    path('certificado/', views.generar_certificado, name='certificado'),
]