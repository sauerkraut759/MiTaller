from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.getCategorias),
    path('categorias/<int:id>/', views.getCategorias),
    path('lugares/', views.getLugares),
    path('lugares/<int:id>', views.getLugares),
    path('profesores/', views.getProfesores),
    path('profesores/<int:id>', views.getProfesores),
    path('talleres/', views.viewTalleres)
]