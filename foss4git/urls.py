from django.conf.urls.defaults import *
from django.contrib import admin
from settings import DEBUG
from settings import STATIC_FILES
from fauna.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fauna/', include('fauna.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^kml/', all_kml),
    (r'^$', italia),
    (r'^regione/(?P<id>[0-9]*)/', regione),
    # TODO (esercizio aggiuntivo, zoom su provincia): (r'^provincia/(?P<id>[0-9]*)/', provincia),
    # TODO (esercizio aggiuntivo, filtrato su animale): (r'^animale/(?P<id>[0-9]*)/', animale),
    # static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_FILES, 'show_indexes': True}),
)

