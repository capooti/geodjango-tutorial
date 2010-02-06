from django.conf.urls.defaults import *
from settings import STATIC_FILES
from fauna.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^foss4git/', include('foss4git.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # indirizzi non soggetti ad autenticazione
    (r'^avvistamenti/', avvistamenti),
    (r'^kml/', all_kml),
    (r'^$', italia),
    (r'^regione/(?P<id>[0-9]*)/', regione),
    # TODO (esercizio aggiuntivo, zoom su provincia): (r'^provincia/(?P<id>[0-9]*)/', provincia),
    # TODO (esercizio aggiuntivo, filtrato su animale): (r'^animale/(?P<id>[0-9]*)/', animale),
    # static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_FILES, 'show_indexes': True}),
)
