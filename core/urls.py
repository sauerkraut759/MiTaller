from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('talleres/todos', views.verTalleres, name='verTalleres'),
    path('talleres/proponer', views.proponerTaller, name='proponerTaller')
]