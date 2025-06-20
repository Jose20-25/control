from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiembroViewSet, FamiliaViewSet, home, ninos_form, jovenes_form, adultos_form, lista_miembros, cumpleaneros_mes, editar_miembro, eliminar_miembro

router = DefaultRouter()
router.register(r'miembros', MiembroViewSet)
router.register(r'familia', FamiliaViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('ninos/', ninos_form, name='ninos_form'),
    path('jovenes/', jovenes_form, name='jovenes_form'),
    path('adultos/', adultos_form, name='adultos_form'),
    path('lista/<str:iglesia>/', lista_miembros, name='lista_miembros'),
    path('cumpleaneros/', cumpleaneros_mes, name='cumpleaneros_mes'),
    path('editar/<int:pk>/', editar_miembro, name='editar_miembro'),
    path('eliminar/<int:pk>/', eliminar_miembro, name='eliminar_miembro'),
    path('api/', include(router.urls)),
]
