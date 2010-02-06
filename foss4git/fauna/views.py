from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.gis.shortcuts import render_to_kml
from fauna.models import *

def avvistamenti(request):
    """vista per visualizzare tutti i punti di avvistamento"""
    avvistamenti  = Avvistamento.objects.all()
    return render_to_response("avvistamenti.html", {'avvistamenti' : avvistamenti})

def all_kml(request):
    """vista per generare il kml di tutti i punti di avvistamento"""
    avvistamenti  = Avvistamento.objects.kml()
    return render_to_kml("gis/kml/placemarks.kml", {'places' : avvistamenti})

def italia(request):
    """vista con zoom su italia e il numero dei punti di avvistamento inseriti nel sistema"""
    num_avvistamenti = Avvistamento.objects.all().count()
    return render_to_response('italia.html', {'num_avvistamenti' : num_avvistamenti})

def regione(request, id):
    """vista con zoom su regione e l'elenco dei punti di avvistamento inseriti nel sistema per la regione in questione"""
    regione = get_object_or_404(Regione, codice=id)
    avvistamenti = Avvistamento.objects.filter(geometry__intersects=regione.geometry)
    return render_to_response("regione.html", { 'regione': regione, 'avvistamenti': avvistamenti })
