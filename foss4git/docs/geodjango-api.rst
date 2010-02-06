==============================
Utilizzo dell'API di GeoDjango
==============================

Creazione di un modello di test
-------------------------------

Aggiungere il seguente modello, che useremo come sandbox per fare un po di test con l'API di GeoDjango::

    class SandboxLayer(gismodels.Model):
        """Modello spaziale per effettuare test con l'API GeoDjango"""
        nome = gismodels.CharField(max_length=50)
        geometry = gismodels.GeometryField(srid=3395) # WGS84 mercatore
        objects = gismodels.GeoManager()

        def __unicode__(self):
            return '%s' % (self.nome)
        
Sincronizzare il database::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py syncdb
    Creating table fauna_sandboxlayer
    Installing index for fauna.SandboxLayer model

Utilizzo dell'API di GeoDjango
------------------------------

Si effettuino alcune prove utilizzando l'API di GeoDjango e verificando i risultati ad es con QGis e il layer SandboxLayer caricato.

Copiamo una regione su sandboxlayer, avendo cura di trasformare il sistema di riferimento della geometria (per accedere alla shell con tutti i path impostati correttamente usare ./manage shell)::

    >>> from fauna.models import *
    >>> lazio = Regione.objects.get(codice=12)
    >>> geom4326 = lazio.geometry
    >>> geom3395 = geom4326.transform(3395, clone=True)
    >>> geom3395.srid
    3395
    >>> geom4326.srid
    4326
    >>> geom3395.envelope.wkt
    'POLYGON ((1274660.3642747686244547 4952975.3447027457877994, 1561642.0010516194161028 4952975.3447027457877994, 1561642.0010516194161028 5258660.0362292015925050, 1274660.3642747686244547 5258660.0362292015925050, 1274660.3642747686244547 4952975.3447027457877994))'
    >>> geom4326.envelope.wkt
    'POLYGON ((11.4504688728938255 40.7864493978667753, 14.0284687786766451 40.7864493978667753, 14.0284687786766451 42.8404801602046703, 11.4504688728938255 42.8404801602046703, 11.4504688728938255 40.7864493978667753))'
    >>> sand_lazio = SandboxLayer(geometry=geom4326,nome='lazio') 
    >>> sand_lazio.save()
    
Analogamente copiamo nel sandboxlayer tutti gli avvistamenti::

    >>> points = Avvistamento.objects.all()
    >>>: for p in points:
       ....:        sand_point = SandboxLayer(geometry=p.geometry.transform(3395,clone=True), nome=p.interesse)
       ....:        sand_point.save()
       ....:
   
Creaimo un buffer utilizzando undo dei punti appena creati sul sandboxlayer::

    >>> p = SandboxLayer.objects.filter(geometry__intersects=sand_lazio.geometry)
    >>> p
    [<SandboxLayer: lazio>, <SandboxLayer: 5>]
    >>> avv = p[1]
    >>>buffer = SandboxLayer(geometry=avv.geometry.buffer(20000),nome='buffer')
    >>>buffer.save()
    
Utilizziamo un operatore spaziale::

    >>>sand_features = SandboxLayer.objects.all()
    >>> sand_features
    [<SandboxLayer: lazio>, <SandboxLayer: 3>, <SandboxLayer: 5>, <SandboxLayer: buffer>]
    >>> sand_features[0].geometry.contains(sand_features[3].geometry)
    True

