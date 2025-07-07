from django.contrib import admin

from .models import Profesor, Categoria, Lugar, Taller
from common.utils import comprobarFeriado

# Register your models here.

class TallerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'fecha',
        'duracion_horas',
        'profesor',
        'lugar',
        'categoria',
        'estado',
        'observacion'
    )

    list_editable = (
        'profesor',
        'estado',
        'observacion'
    )

    actions = ['aceptar', 'rechazar', 'revisar']

    def aceptar(self, request, queryset):
        for taller in queryset:
            taller.estado = 'aceptado'
            taller.save()

        self.message_user(request, f"{queryset.count()} nuevos talleres aceptados.")

    def rechazar(self, request, queryset):
        for taller in queryset:
            taller.estado = 'rechazado'
            taller.save()

        self.message_user(request, f"{queryset.count()} nuevos talleres rechazados.")

    def revisar(self, request, queryset):
        for taller in queryset:
            taller.estado = 'pendiente'
            taller.save()

        self.message_user(request, f"{queryset.count()} nuevos talleres marcados para revision.")

    def save_model(self, request, obj, form, change):

        if not change:
            data_comprobada = comprobarFeriado(obj.fecha, obj.categoria)

            obj.estado = data_comprobada['estado']
            obj.observacion = data_comprobada['observacion']


        return super().save_model(request, obj, form, change)
        


admin.site.register(Profesor)
admin.site.register(Categoria)
admin.site.register(Lugar)
admin.site.register(Taller, TallerAdmin)