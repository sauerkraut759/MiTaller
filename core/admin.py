from django.contrib import admin
from .models import Profesor, Categoria, Lugar, Taller

# Register your models here.


admin.site.register(Profesor)
admin.site.register(Categoria)
admin.site.register(Lugar)
admin.site.register(Taller)