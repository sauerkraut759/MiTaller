from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from core.models import Categoria, Lugar, Profesor, Taller
from .serializers import CategoriaSerializer, ProfesorSerializer, LugarSerializer, TallerSerializer

# Create your views here.

@api_view(['GET'])
def getCategorias(request, id=0):

    if id != 0:
        categorias = Categoria.objects.get(id=id)
        serializer = CategoriaSerializer(categorias, many=False)
    else:
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

    
    return Response(serializer.data)

@api_view(['GET'])
def getProfesores(request, id=0):

    if id != 0:
        profesores = Profesor.objects.get(id=id)
        serializer = ProfesorSerializer(profesores, many=False)
    else:
        profesores = Profesor.objects.all()
        serializer = ProfesorSerializer(profesores, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getLugares(request):
    
    if id != 0:
        lugares = Lugar.objects.get(id=id)
        serializer = LugarSerializer(lugares, many=False)
    else:
        lugares = Lugar.objects.all()
        serializer = LugarSerializer(lugares, many=True)
    
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def viewTalleres(request):

    if request.method == 'GET':

        estado = request.query_params.get('estado')
        futuros = request.query_params.get('futuros')

        # Si es anonimo o pide solo los futuros devuelve lo correspondiente y si pide un estado especifico lo filtra (estando autenticado)
        if request.user.is_anonymous or futuros:
            talleres = Taller.objects.filter(estado='aceptado', fecha__gte=timezone.now().date())
        elif futuros:
            talleres = Taller.objects.filter(estado=estado)
        else:
            talleres = Taller.objects.all()

    
    serializer = TallerSerializer(talleres, many=True)
    
    return Response(serializer.data)