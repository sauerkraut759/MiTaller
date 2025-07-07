import requests
from datetime import datetime

def comprobarFeriado(fecha_taller, categoria):

    data = {
        'estado': 'pendiente',
        'observacion': ''
    }

    try:
        res = requests.get('https://api.boostr.cl/holidays.json')
        res.raise_for_status()
        feriados = res.json()['data']
    except requests.exceptions.RequestException as e:
        print("Error al consultar API de feriados")
        return None

    for feriado in feriados:
        fecha = datetime.fromisoformat(feriado['date']).date()

        if fecha_taller.date() == fecha:
            if feriado['inalienable']:
                data['estado'] = 'rechazado'
                data['observacion'] = 'No se programan talleres en feriados irrenunciables'
            elif categoria.id != 1:
                data['estado']='rechazado'
                data['observacion'] = 'Solo se programan talleres al aire libre en feriados'

            break

    return data