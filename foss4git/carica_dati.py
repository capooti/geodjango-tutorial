"""Utility per inserire regioni e province sul database dagli shapefile allegati"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.gis.utils import mapping, LayerMapping
from fauna.models import Regione, Provincia

print 'carico regioni...'

regioni_mapping = {
    'codice' : 'cod_reg',
    'nome' : 'regione',
    'geometry' : 'MULTIPOLYGON',
}

regioni_shp = 'data/shapefile/regioni.shp'
regioni =  LayerMapping(Regione, regioni_shp, regioni_mapping, transform=False, encoding='iso-8859-1')
regioni.save(verbose=True, progress=True)

print 'carico province...'

province_mapping = {
    'codice' : 'cod_prov',
    'nome' : 'provincia',
    'geometry' : 'MULTIPOLYGON',
}

province_shp = 'data/shapefile/province.shp'
province =  LayerMapping(Provincia, province_shp, province_mapping, transform=False, encoding='iso-8859-1')
province.save(verbose=True, progress=True)
