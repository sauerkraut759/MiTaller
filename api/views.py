from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Categoria, Lugar, Profesor, Taller
from .serializers import CategoriaSerializer, ProfesorSerializer, LugarSerializer, TallerSerializer

# Create your views here.

@api_view(['GET'])
def getCategorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getProfesores(request):
    profesores = Profesor.objects.all()
    serializer = ProfesorSerializer(profesores, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getLugares(request):
    lugares = Lugar.objects.all()
    serializer = LugarSerializer(lugares, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def viewTalleres(request):

    estado = request.query_params.get('estado')
    if estado:
        talleres = Taller.objects.filter(estado=estado)
    else:
        talleres = Taller.objects.all()

    serializer = TallerSerializer(talleres, many=True)
    
    
    return Response(serializer.data)