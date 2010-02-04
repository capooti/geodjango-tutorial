from django.contrib.gis.admin import GeoModelAdmin
from django.contrib import admin
from models import *

class AvvistamentoAdmin(GeoModelAdmin):

    model = Avvistamento

    list_display = ['data', 'animale', 'interesse']
    list_filter = ['data', 'animale', 'interesse']
    date_hierarchy = 'data'
    fieldsets = (
      ('Location Attributes', {'fields': (('data', 'animale', 'note', 'interesse'))}),
      ('Editable Map View', {'fields': ('geometry',)}),
    )

    # Openlayers settings
    scrollable = False
    map_width = 500
    map_height = 500
    openlayers_url = '/static/openlayers/lib/OpenLayers.js'
    default_zoom = 6
    default_lon = 13
    default_lat = 42

class AnimaleAdmin(admin.ModelAdmin):

    model = Animale
    list_display = ['nome', 'image_url',]

# registriamo per l'admin
admin.site.register(Animale, AnimaleAdmin)
admin.site.register(Avvistamento, AvvistamentoAdmin)
