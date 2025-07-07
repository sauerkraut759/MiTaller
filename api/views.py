import requests
from datetime import datetime
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
        elif estado:
            talleres = Taller.objects.filter(estado=estado)
        else:
            talleres = Taller.objects.all()
            print(talleres.count())

        serializer = TallerSerializer(talleres, many=True)
    
        return Response(serializer.data)

    if request.method == 'POST':
        if request.user.is_anonymous:
            return Response({'message': 'debe estar autenticado para hacer esta request'}, status=401)
        
        serializer = TallerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        data = serializer.validated_data
        fecha_taller = data['fecha']
        categoria = data['categoria']
        estado = 'pendiente'
        observacion = ''
            
        try:
            res = requests.get('https://api.boostr.cl/holidays.json')
            res.raise_for_status()
            feriados = res.json()['data']
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Error al consultar api de feriados'}, status=502)

        for feriado in feriados:
            fecha = datetime.fromisoformat(feriado['date']).date()

            if fecha_taller.date() == fecha:
                if feriado['inalienable']:
                    estado = 'rechazado'
                    observacion = 'No se programan talleres en feriados irrenunciables'
                elif categoria.id != 1:
                    estado='rechazado'
                    observacion = 'Solo se programan talleres al aire libre en feriados'

                break

        taller = serializer.save(estado=estado, observacion=observacion)

        return Response(TallerSerializer(taller).data, status=201)
    
    return Response(status=404)


    
    