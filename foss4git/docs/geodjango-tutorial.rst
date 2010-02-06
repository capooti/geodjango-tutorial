=====================
Utilizzo di GeoDjango
=====================

Importazione di GeoDjango
-------------------------

Aggiungere l'applicazione contrib.gis nel file settings.py del progetto::

    ...
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.admin',
        'django.contrib.gis',
        'foss4git.fauna',
    )
    ...
    
Aggiunta del campo geometrico nel modello
-----------------------------------------

Vogliamo aggiungere un campo geometrico puntuale nel modello Avvistamento.
Per fare questa cosa bisogna far ereditare il modello a django.contrib.gis.db anziche' a django.db.models.
Una volta' fatto cio' sara' possibile usare il campo geometrico.
Ricordarsi di abilitare models.GeoManager al posto del manager di default (models.objects) per avere a disposizione tutte le funzionalita' di geodjango sul modello.

Effettuare le seguenti modifiche su models.py::

    from django.db import models
    from django.contrib.gis.db import models as gismodels

    # modelli
    class Animale(models.Model):
        """Modello per rappresentare gli animali"""
        nome = models.CharField(max_length=50)
    ...
    class Avvistamento(gismodels.Model):
        """Modello spaziale per rappresentare gli avvistamenti"""

        LIVELLI_INTERESSE = (
            (1, '*'),
            (2, '**'),
            (3, '***'),
            (4, '****'),
            (5, '*****'),
        )
        data = gismodels.DateTimeField()
        note = gismodels.TextField()
        interesse = gismodels.IntegerField(choices=LIVELLI_INTERESSE)
        animale = gismodels.ForeignKey(Animale)
        geometry = gismodels.PointField(srid=4326) 
        objects = gismodels.GeoManager()
    ...

Prima di effettuare la sincronizzazione e' necessario cancellare la tabella fauna_avvistamento::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ psql -U geodjango tutorial
    psql (8.4.2)
    Type "help" for help.

    tutorial=> drop table fauna_avvistamento;
    DROP TABLE
    
A questo punto sincronizzare il database::
    
    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py syncdb
    Creating table fauna_avvistamento
    Installing index for fauna.Avvistamento model
    
Gestire dati geometrici nell'admin
----------------------------------
    
Dobbiamo abilitare l'applicazione admin a gestire il data entry del dato geometrico. Useremo la funzionalita' di GeoDjango che abilita l'editing dei dati geografici utilizzando OpenLayers su cartografia OpenStreetMap.

Per far questo modifichiamo il file admin.py::

    from django.contrib import admin
    from django.contrib.gis.admin import GeoModelAdmin
    from models import *

    class AvvistamentoAdmin(GeoModelAdmin):

        model = Avvistamento

        list_display = ['data', 'animale', 'interesse']
        list_filter = ['data', 'animale', 'interesse']
        date_hierarchy = 'data'
        fieldsets = (
          ('Caratteristiche avvistamento', {'fields': (('data', 'animale', 'note', 'interesse'))}),
          ('Mappa', {'fields': ('geometry',)}),
        )

        # Openlayers settings
        scrollable = False
        map_width = 500
        map_height = 500
        #openlayers_url = '/static/openlayers/lib/OpenLayers.js'
        default_zoom = 6
        default_lon = 13
        default_lat = 42

    class AnimaleAdmin(admin.ModelAdmin):
    ...

Importazione di shapefile
-------------------------

A questo punto creiamo due geomodelli per la gestione delle regioni e delle province.

I dati relativi a regioni e province sono nei due shapefile omonimi sotto la directory data/shapefiles e sono georiferiti nel sistema geografico WGS 1984 (srid=4326).

Possiamo analizzare i due shapefiles con l'utility orginfo presente nel pacchetto GDAL/OGR (usando l'opzione so, summary only)::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ogrinfo data/shapefile/regioni.shp regioni -so
    INFO: Open of `data/shapefile/regioni.shp'
          using driver `ESRI Shapefile' successful.

    Layer name: regioni
    Geometry: Polygon
    Feature Count: 20
    Extent: (6.627586, 35.493472) - (18.521529, 47.093684)
    Layer SRS WKT:
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            TOWGS84[0,0,0,0,0,0,0],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
        AUTHORITY["EPSG","4326"]]
    gid: Integer (10.0)
    objectid: Integer (10.0)
    regione: String (255.0)
    cod_rip1: Integer (10.0)
    cod_rip2: Integer (10.0)
    cod_reg: Integer (10.0)
    shape_area: Real (24.15)
    shape_len: Real (24.15)
    boundingbo: String (255.0)
    
    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ogrinfo data/shapefile/province.shp province -so
    INFO: Open of `data/shapefile/province.shp'
      using driver `ESRI Shapefile' successful.

    Layer name: province
    Geometry: Polygon
    Feature Count: 107
    Extent: (6.627586, 35.493472) - (18.521529, 47.093684)
    Layer SRS WKT:
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            TOWGS84[0,0,0,0,0,0,0],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
        AUTHORITY["EPSG","4326"]]
    gid: Integer (10.0)
    objectid: Integer (10.0)
    cod_prov: Integer (10.0)
    cod_ipi: Integer (10.0)
    provincia: String (255.0)
    sigla: String (255.0)
    cod_reg: Integer (10.0)
    shape_area: Real (24.15)
    shape_len: Real (24.15)
    boundingbo: String (255.0)

In entrambi i casi importeremo i campi relativi a nome, codice (regione e cod_reg per regioni, provincia e cod_prov per province) e geometria.

Come prima cosa aggiungiamo i due geomodelli che gestiscono le entita' Regione e Provincia::

    class Regione(gismodels.Model):
        """Modello spaziale per rappresentare le regioni"""
        codice = gismodels.IntegerField()
        nome = gismodels.CharField(max_length=50)
        geometry = gismodels.MultiPolygonField(srid=4326) 
        objects = gismodels.GeoManager()

        def __unicode__(self):
            return '%s' % (self.nome)

    class Provincia(gismodels.Model):
        """Modello spaziale per rappresentare le regioni"""
        codice = gismodels.IntegerField()
        nome = gismodels.CharField(max_length=50)
        geometry = gismodels.MultiPolygonField(srid=4326) 
        objects = gismodels.GeoManager()

        def __unicode__(self):
            return '%s' % (self.nome)

Prima di effettuare la sincronizzazione del database, verifichiamo gli oggetti che verranno creati nel database::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py sql fauna
    BEGIN;
    CREATE TABLE "fauna_animale" (
        "id" serial NOT NULL PRIMARY KEY,
        "nome" varchar(50) NOT NULL,
        "foto" varchar(100) NOT NULL
    )
    ;
    CREATE TABLE "fauna_avvistamento" (
        "id" serial NOT NULL PRIMARY KEY,
        "data" timestamp with time zone NOT NULL,
        "note" text NOT NULL,
        "interesse" integer NOT NULL,
        "animale_id" integer NOT NULL REFERENCES "fauna_animale" ("id") DEFERRABLE INITIALLY DEFERRED
    )
    ;
    CREATE TABLE "fauna_regione" (
        "id" serial NOT NULL PRIMARY KEY,
        "codice" integer NOT NULL,
        "nome" varchar(50) NOT NULL
    )
    ;
    CREATE TABLE "fauna_provincia" (
        "id" serial NOT NULL PRIMARY KEY,
        "codice" integer NOT NULL,
        "nome" varchar(50) NOT NULL
    )
    ;
    COMMIT;

A questo punto sincronizziamo il database::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py syncdb
    Creating table fauna_regione
    Creating table fauna_provincia
    Installing index for fauna.Regione model
    Installing index for fauna.Provincia model
    
Creiamo uno script carica_dati.py per importare i due shapefile nel database spaziale usando l'utility di GeoDjango LayerMapping::

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

Lanciamo lo script per effettuare il caricamento::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ python carica_dati.py 
    carico regioni...
    Saved: PIEMONTE
    Saved: VALLE D'AOSTA
    ...
    Saved: LOMBARDIA
    Saved: LAZIO
    carico province...
    Saved: TORINO
    Saved: VERCELLI
    ...
    Saved: MEDIO CAMPIDANO
    Saved: CARBONIA-IGLESIAS

Creazione di template con OpenLayer e GeoDjango
-----------------------------------------------

Creeremo due template che mostrano l'utilizzo di OpenLayers e GeoDjango::

* un template denominato italia.html, generato dalla view italia che visualizza tutti i punti di avvistamento sul territorio nazionale
* un template denominato regione.html, generato dalla view regione che visualizza tutti i punti di avvistamento sul territorio regionale e ne fornisce l'elenco

Se avanza tempo provare a creare un template che visualizzi i punti per provincia ed una vista che visualizzi i punti per tipologia di animale avvistato.

Inoltre creeremo una view denominata all_kml che alimenta il template di geodjango gis/kml/placemarks.kml. Tale view fornisce un elenco completo in formato kml delle geometrie inserite nel sistema che servira' ad alimentare il layer vettoriale di OpenLayers per la visualizzazione degli avvistamenti sulla mappa.

Come prima cosa dichiariamo queste tre view sul file urls.py::

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

A questo punto creiamo le tre view necessarie sul file views.py::

    from django.shortcuts import render_to_response, get_object_or_404
    from django.contrib.gis.shortcuts import render_to_kml
    from fauna.models import *

    def avvistamenti(request):
        ...

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
        
Infine creiamo i due template necessari: italia.html e regione.html.

Notare che, nel caso non ci fosse una connessione internet, abbiamo creato un WMS con mapserver da utilizzare come base layer al posto del basic layer del WMS di Metacarta.

italia.html::

    <html>
      <head>
        <script src="/static/openlayers/lib/OpenLayers.js"></script>
        <style type="text/css"> #map { width:500px; height: 500px; } </style>
        <script type="text/javascript">
            var map, base_layer, kml;
            var ms_url = "http://localhost/cgi-bin/mapserv?map=/home/geodjango/tutorial/django-1.2-alpha-1-env/foss4git/mapserver/italia.map&"
            function init(){
                map = new OpenLayers.Map('map');
                base_layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
                   "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
                var regioni = new OpenLayers.Layer.WMS("Regioni",
                   ms_url, {layers : 'regioni'} );
                var province = new OpenLayers.Layer.WMS("Province",
                   ms_url, {layers : 'province'} );

                kml = new OpenLayers.Layer.GML("KML", "/kml", 
                   { format: OpenLayers.Format.KML });
                map.addLayers([base_layer, regioni, province, kml]);
                
                map.addControl(new OpenLayers.Control.LayerSwitcher());
                map.setCenter(new OpenLayers.LonLat(13,42),6); 
                }
        </script>
      </head>
      <body onload="init()">
        <h3>Avvistamenti in Italia</h3>
        <div id="map"></div>
        <p>Sono stati inseriti {{num_avvistamenti}} avvistamenti.</p>
      </body>
    </html>

regione.html::

    <html>
      <head>
        <script src="http://openlayers.org/api/OpenLayers.js"></script>
        <style type="text/css"> #map { width:400px; height: 400px; } </style>
        <script type="text/javascript">
            var map, base_layer, kml;
            var ms_url = "http://localhost/cgi-bin/mapserv?map=/home/geodjango/tutorial/django-1.2-alpha-1-env/foss4git/mapserver/italia.map&"
            function init(){
                map = new OpenLayers.Map('map');
                base_layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
                   "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
                var regioni = new OpenLayers.Layer.WMS("Regioni",
                   ms_url, {layers : 'regioni'} );
                var province = new OpenLayers.Layer.WMS("Province",
                   ms_url, {layers : 'province'} );

                var format = new OpenLayers.Format.GeoJSON()
                regione = format.read({{ regione.geometry.geojson|safe}})[0]; 
                // We mark it 'safe' so that Django doesn't escape the quotes.
                
                regione.attributes = { 'nome': "{{regione.nome}}", 'type': 'regione'}; 
                vectors = new OpenLayers.Layer.Vector("Data");
                vectors.addFeatures(regione); 
                for (var i = 0; i < points.length; i++) {
                    point = format.read(points[i])[0]; 
                    point.attributes = {'type':'point'}; 
                    vectors.addFeatures(point);
                }
                map.addLayers([base_layer, regioni, province, vectors]);
                
                map.addControl(new OpenLayers.Control.LayerSwitcher());
                map.zoomToExtent(regione.geometry.getBounds());
    }
        </script>
      </head>
      <body onload="init()">
        <h3>Avvistamenti nella regione: {{ regione.nome}}</h3>
        <div id="map"></div>
        In questa regione ci sono stati {{avvistamenti.count}} avvistamenti.<br>
        <script> var points = []; </script>
        <ul>
        {% for avvistamento in avvistamenti %}
            <li>{{ avvistamento.data }}, {{ avvistamento.animale.nome }}</li>
            <script>points.push({{avvistamento.geometry.geojson|safe}});</script>
        {% endfor %}
        </ul>
      </body>
    </html>

A questo punto eventualmente rilanciare il server di django e verificare che le viste in questione presentino i risultati previsti.

