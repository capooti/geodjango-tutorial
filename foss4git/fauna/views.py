from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.gis.shortcuts import render_to_kml
from fauna.models import *

# vista per generare il kml di tutti i punti di avvistamento
def all_kml(request):
    avvistamenti  = Avvistamento.objects.kml()
    return render_to_kml("gis/kml/placemarks.kml", {'places' : avvistamenti})

# vista con zoom su italia e il numero dei punti di avvistamento inseriti nel sistema
def italia(request):
    num_avvistamenti = Avvistamento.objects.all().count()
    return render_to_response('italia.html', {'num_avvistamenti' : num_avvistamenti})

def regione(request, id):
    #regione = get_object_or_404(Regione, pk=id)
    regione = get_object_or_404(Regione, codice=id)
    avvistamenti = Avvistamento.objects.filter(geometry__intersects=regione.geometry)
    return render_to_response("regione.html", { 'regione': regione, 'avvistamenti': avvistamenti })
