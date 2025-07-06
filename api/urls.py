from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.getCategorias),
    path('lugares/', views.getLugares),
    path('profesores/', views.getProfesores),
    path('talleres/', views.viewTalleres)
]