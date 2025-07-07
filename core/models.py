from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Lugar(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Taller(models.Model):

    ESTADOS = [
        ('pendiente', 'En Revision'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado')
    ]


    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    duracion_horas = models.DecimalField(max_digits=4, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="pendiente")

    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    observacion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.titulo}"
